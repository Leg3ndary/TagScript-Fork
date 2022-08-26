from __future__ import annotations

import logging
from itertools import islice
from typing import Any, Dict, List, Optional, Tuple, Union

from .exceptions import (
    BlocknameDuplicateError,
    ProcessError,
    StopError,
    TagScriptError,
    WorkloadExceededError,
)
from .interface import Adapter, Block
from .utils import maybe_await
from .verb import Verb

__all__ = (
    "Interpreter",
    "AsyncInterpreter",
    "Context",
    "Response",
    "Node",
    "build_node_tree",
)

log = logging.getLogger(__name__)

AdapterDict = Dict[str, Adapter]


class Node:
    """
    A low-level object representing a bracketed block.

    Attributes
    ----------
    coordinates: Tuple[int, int]
        The start and end position of the bracketed text block.
    verb: Optional[Verb]
        The determined Verb for this node.
    output:
        The `Block` processed output for this node.
    """

    __slots__ = ("output", "verb", "coordinates")

    def __init__(self, coordinates: Tuple[int, int], verb: Optional[Verb] = None) -> None:
        """
        Constructing the Node
        """
        self.coordinates = coordinates
        self.verb = verb
        self.output: Optional[str] = None

    def __str__(self) -> str:
        """
        String function
        """
        return str(self.verb) + " at " + str(self.coordinates)

    def __repr__(self) -> str:
        """
        String repr
        """
        return f"<Node verb={self.verb!r} coordinates={self.coordinates!r} output={self.output!r}>"


def build_node_tree(message: str) -> List[Node]:
    """
    Function that finds all possible nodes in a string.

    Parameters
    ----------
    message: str
        The string to find nodes in.

    Returns
    -------
    List[Node]
        A list of all possible text bracket blocks.
    """
    nodes = []
    # previous = r""

    starts = []
    for i, ch in enumerate(message):
        if ch == "{":  # and previous[1:] != "\\":
            starts.append(i)
        if ch == "}":  # and previous[1:] != "\\":
            if not starts:
                continue
            coords = (starts.pop(), i)
            n = Node(coords)
            nodes.append(n)

        # previous = previous[:1] + ch
    return nodes


class Response:
    """
    An object containing information on a completed TagScript process.

    Attributes
    ----------
    body: str
        The cleaned message with all verbs interpreted.
    actions: Dict[str, Any]
        A dictionary that blocks can access and modify to define post-processing actions.
    variables: Dict[str, Adapter]
        A dictionary of variables that blocks such as the `LooseVariableGetterBlock` can access.
    extras: Dict[str, Any]
        A dictionary of extra keyword arguments that blocks can use to define their own behavior.
    """

    __slots__ = ("body", "actions", "variables", "extras")

    def __init__(self, *, variables: AdapterDict = None, extras: Dict[str, Any] = None) -> None:
        """
        Construct the response
        """
        self.body: str = None
        self.actions: Dict[str, Any] = {}
        self.variables: AdapterDict = variables if variables is not None else {}
        self.extras: Dict[str, Any] = extras if extras is not None else {}

    def __repr__(self) -> str:
        """
        String repr
        """
        return f"<Response body={self.body!r} actions={self.actions!r} variables={self.variables!r} extras={self.extras!r}>"


class Context:
    """
    An object containing data on the TagScript block processed by the interpreter.
    This class is passed to adapters and blocks during processing.

    Attributes
    ----------
    verb: Verb
        The Verb object representing a TagScript block.
    original_message: str
        The original message passed to the interpreter.
    interpreter: Interpreter
        The interpreter processing the TagScript.
    """

    __slots__ = ("verb", "original_message", "interpreter", "response")

    def __init__(self, verb: Verb, res: Response, interpreter: Interpreter, og: str) -> None:
        """
        Construct the context
        """
        self.verb: Verb = verb
        self.original_message: str = og
        self.interpreter: Interpreter = interpreter
        self.response: Response = res

    def __repr__(self) -> str:
        """
        String repr
        """
        return f"<Context verb={self.verb!r}>"


class Interpreter:
    """
    The TagScript interpreter.

    Attributes
    ----------
    blocks: UnionList[Block]
        A list or tuple of blocks to be used for TagScript processing.
    """

    __slots__ = ("blocks", "_blocknames")

    def __init__(self, blocks: Union[List[Block], Tuple[Block]]) -> None:
        """
        Creates a list of blocks, and also gets all acceptable names for processing

        Raises
        ------
        BlocknameDuplicateError
            If there are duplicate blocknames.
        """
        self.blocks: Union[List[Block], Tuple[Block]] = blocks
        self._blocknames = []
        for block in blocks:
            for name in block.ACCEPTED_NAMES:
                if block in self._blocknames:
                    raise BlocknameDuplicateError(block)
                self._blocknames.append(name)

    def __repr__(self) -> str:
        """
        String repr
        """
        return f"<{type(self).__name__} blocks={self.blocks!r}>"

    def _get_context(
        self,
        node: Node,
        final: str,
        *,
        response: Response,
        original_message: str,
        verb_limit: int,
    ) -> Context:
        """
        Construct a context object for a node.

        Parameters
        ----------
        node: Node
            The node to construct the context for.
        final: str
            The final message to be processed.
        response: Response
            The response object to be passed to the context.
        original_message: str
            The original message passed to the interpreter.
        verb_limit: int
            The maximum number of verbs to process.

        Returns
        -------
        Context
            The constructed context.
        """
        # Get the updated verb string from coordinates and make the context
        start, end = node.coordinates
        node.verb = Verb(final[start : end + 1], limit=verb_limit)
        return Context(node.verb, response, self, original_message)

    def _get_acceptors(self, ctx: Context) -> Tuple[Block]:
        """
        Get a list of acceptors

        Parameters
        ----------
        ctx: Context
            The context to get the acceptors for.

        Returns
        -------
        Tuple[Block]
        """
        acceptors = (b for b in self.blocks if b.will_accept(ctx))
        log.debug("%r acceptors: %r", ctx, acceptors)
        return acceptors

    def _process_blocks(self, ctx: Context, node: Node) -> Optional[str]:
        """
        Process the blocks

        Parameters
        ----------
        ctx: Context
            The context to process the blocks from.
        node: Node
            The node to process the blocks from.

        Returns
        -------
        Optional[str]
            The final message
        """
        acceptors = self._get_acceptors(ctx)
        for b in acceptors:
            value = b.process(ctx)
            if value is not None:  # Value found? We're done here.
                value = str(value)
                node.output = value
                return value
        return None

    @staticmethod
    def _check_workload(charlimit: int, total_work: int, output: str) -> Optional[int]:
        """
        Check if the workload has been exceeded.

        Parameters
        ----------
        charlimit: int
            The maximum number of characters to process.
        total_work: int
            The total number of characters processed.
        output: str
            The output string.

        Returns
        -------
        Optional[int]
            The total amount of work that has been processed.

        Raises
        ------
        WorkloadExceededError
            If the workload has been exceeded.
        """
        if not charlimit:
            return None
        total_work += len(output)
        if total_work > charlimit:
            raise WorkloadExceededError(
                "The TSE interpreter had its workload exceeded. The total characters "
                f"attempted were {total_work}/{charlimit}"
            )
        return total_work

    @staticmethod
    def _text_deform(start: int, end: int, final: str, output: str) -> Tuple[str, int]:
        """
        Deform the text, replacing code with what was outputted.

        Parameters
        ----------
        start: int
            The start index of the code.
        end: int
            The end index of the code.
        final: str
            The final message.
        output: str
            The output string.

        Returns
        -------
        Tuple[str, int]
            The new final message, and the change in final length after the change has been applied.
        """
        message_slice_len = (end + 1) - start
        replacement_len = len(output)
        differential = (
            replacement_len - message_slice_len
        )  # The change in size of `final` after the change is applied
        final = final[:start] + output + final[end + 1 :]
        return final, differential

    @staticmethod
    def _translate_nodes(
        node_ordered_list: List[Node], index: int, start: int, differential: int
    ) -> None:
        """
        Get the new coordinates for each node.

        Parameters
        ----------
        node_ordered_list: List[Node]
            The list of nodes to translate.
        index: int
            The index of the node to translate.
        start: int
            The start index of the code.
        differential: int
            The change in final length after the change has been applied.

        Returns
        -------
        None
        """
        for future_n in islice(node_ordered_list, index + 1, None):
            new_start = None
            new_end = None
            if future_n.coordinates[0] > start:
                new_start = future_n.coordinates[0] + differential
            else:
                new_start = future_n.coordinates[0]

            if future_n.coordinates[1] > start:
                new_end = future_n.coordinates[1] + differential
            else:
                new_end = future_n.coordinates[1]
            future_n.coordinates = (new_start, new_end)

    def _solve(
        self,
        message: str,
        node_ordered_list: List[Node],
        response: Response,
        *,
        charlimit: int,
        verb_limit: int = 2000,
    ) -> Optional[str]:
        """
        Solve the tagscript by proccessing all possible nodes.

        Parameters
        ----------
        message: str
            The message to process.
        node_ordered_list: List[Node]
            The list of nodes to process.
        response: Response
            The response object to be passed to the context.
        charlimit: int
            The maximum number of characters to process.
        verb_limit: int
            The maximum number of verbs to process.

        Returns
        -------
        Optional[str]
            The final, completely processed message.
        """
        final = message
        total_work = 0
        for index, node in enumerate(node_ordered_list):
            start, end = node.coordinates
            ctx = self._get_context(
                node,
                final,
                response=response,
                original_message=message,
                verb_limit=verb_limit,
            )
            log.debug("Processing context %r at (%r, %r)", ctx, start, end)
            try:
                output = self._process_blocks(ctx, node)
            except StopError as exc:
                log.debug("StopError raised on node %r", node, exc_info=exc)
                return final[:start] + exc.message
            if output is None:
                continue  # If there was no value output, no need to text deform.

            total_work = self._check_workload(charlimit, total_work, output)
            final, differential = self._text_deform(start, end, final, output)
            self._translate_nodes(node_ordered_list, index, start, differential)
        return final

    @staticmethod
    def _return_response(response: Response, output: str) -> Response:
        """
        Return the response object.

        Parameters
        ----------
        response: Response
            The response object to be returned.
        output: str
            The output string.

        Returns
        -------
        Response
            The response object.
        """
        if response.body is None:
            response.body = output.strip()
        else:
            # Dont override an overridden response.
            response.body = response.body.strip()
        return response

    def process(
        self,
        message: str,
        seed_variables: AdapterDict = None,
        *,
        charlimit: Optional[int] = None,
        **kwargs,
    ) -> Response:
        """
        Processes a given TagScript string.

        Parameters
        ----------
        message: str
            A TagScript string to be processed.
        seed_variables: Dict[str, Adapter]
            A dictionary containing strings to adapters to provide context variables for processing.
        charlimit: int
            The maximum characters to process.
        kwargs: Dict[str, Any]
            Additional keyword arguments that may be used by blocks during processing.

        Returns
        -------
        Response
            A response object containing the processed body, actions and variables.

        Raises
        ------
        TagScriptError
            A block intentionally raised an exception, most likely due to invalid user input.
        WorkloadExceededError
            Signifies the interpreter reached the character limit, if one was provided.
        ProcessError
            An unexpected error occurred while processing blocks.
        """
        response = Response(variables=seed_variables, extras=kwargs)
        node_ordered_list = build_node_tree(message)
        try:
            output = self._solve(
                message,
                node_ordered_list,
                response,
                charlimit=charlimit,
            )
        except TagScriptError:
            raise
        except Exception as error:
            raise ProcessError(error, response, self) from error
        return self._return_response(response, output)


class AsyncInterpreter(Interpreter):
    """
    An asynchronous subclass of `Interpreter` that allows blocks to implement asynchronous methods.
    Synchronous blocks are still supported.
    This subclass has no additional attributes from the `Interpreter` class.
    See `Interpreter` for full documentation.
    """

    async def _get_acceptors(self, ctx: Context) -> Tuple[Block]:
        """
        Get a list of acceptors

        Parameters
        ----------
        ctx: Context
            The context to get the acceptors for.

        Returns
        -------
        Tuple[Block]
        """
        return (b for b in self.blocks if await maybe_await(b.will_accept, ctx))

    async def _process_blocks(self, ctx: Context, node: Node) -> Optional[str]:
        """
        Process the blocks

        Parameters
        ----------
        ctx: Context
            The context to process the blocks from.
        node: Node
            The node to process the blocks from.

        Returns
        -------
        Optional[str]
            The final message
        """
        acceptors = await self._get_acceptors(ctx)
        for b in acceptors:
            value = await maybe_await(b.process, ctx)
            if value is not None:  # Value found? We're done here.
                value = str(value)
                node.output = value
                return value

    async def _solve(
        self,
        message: str,
        node_ordered_list: List[Node],
        response: Response,
        *,
        charlimit: int,
        verb_limit: int = 2000,
    ) -> Optional[str]:
        """
        Solve the tagscript by proccessing all possible nodes.

        Parameters
        ----------
        message: str
            The message to process.
        node_ordered_list: List[Node]
            The list of nodes to process.
        response: Response
            The response object to be passed to the context.
        charlimit: int
            The maximum number of characters to process.
        verb_limit: int
            The maximum number of verbs to process.

        Returns
        -------
        Optional[str]
            The final, completely processed message.
        """
        final = message
        total_work = 0

        for index, node in enumerate(node_ordered_list):
            start, end = node.coordinates
            ctx = self._get_context(
                node,
                final,
                response=response,
                original_message=message,
                verb_limit=verb_limit,
            )
            try:
                output = await self._process_blocks(ctx, node)
            except StopError as exc:
                return final[:start] + exc.message
            if output is None:
                continue  # If there was no value output, no need to text deform.

            total_work = self._check_workload(charlimit, total_work, output)
            final, differential = self._text_deform(start, end, final, output)
            self._translate_nodes(node_ordered_list, index, start, differential)
        return final

    async def process(
        self,
        message: str,
        seed_variables: AdapterDict = None,
        *,
        charlimit: Optional[int] = None,
        **kwargs,
    ) -> Response:
        """
        Asynchronously process a given TagScript string.
        This method has no additional attributes from the `Interpreter` class.
        See `Interpreter.process` for full documentation.
        """
        response = Response(variables=seed_variables, extras=kwargs)
        node_ordered_list = build_node_tree(message)
        try:
            output = await self._solve(
                message,
                node_ordered_list,
                response,
                charlimit=charlimit,
            )
        except TagScriptError:
            raise
        except Exception as error:
            raise ProcessError(error, response, self) from error
        return self._return_response(response, output)
