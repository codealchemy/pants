# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os

from pants.base.specs import AddressSpec, DescendantAddresses, SiblingAddresses, SingleAddress


class CmdLineSpecParser:
  """Parses address selectors as passed from the command line.

  See the `specs` package for more information on the types of objects returned.
  This class supports some flexibility in the path portion of the spec to allow for more natural
  command line use cases like tab completion leaving a trailing / for directories and relative
  paths, ie both of these::

    ./src/::
    /absolute/path/to/project/src/::

  Are valid command line specs even though they are not a valid BUILD file specs.  They're both
  normalized to::

    src::

  The above expression would choose every target under src.
  """

  class BadSpecError(Exception):
    """Indicates an unparseable command line address selector."""

  def __init__(self, root_dir: str) -> None:
    self._root_dir = os.path.realpath(root_dir)

  def _normalize_spec_path(self, path: str) -> str:
    is_abs = not path.startswith('//') and os.path.isabs(path)
    if is_abs:
      path = os.path.realpath(path)
      if os.path.commonprefix([self._root_dir, path]) != self._root_dir:
        raise self.BadSpecError('Absolute address path {0} does not share build root {1}'
                                .format(path, self._root_dir))
    else:
      if path.startswith('//'):
        path = path[2:]
      path = os.path.join(self._root_dir, path)

    normalized = os.path.relpath(path, self._root_dir)
    if normalized == '.':
      normalized = ''
    return normalized

  def parse_address_spec(self, spec: str) -> AddressSpec:
    """Parse the given spec into an `AddressSpec` object.

    :raises: CmdLineSpecParser.BadSpecError if the address selector could not be parsed.
    """

    if spec.endswith('::'):
      spec_path = spec[:-len('::')]
      return DescendantAddresses(self._normalize_spec_path(spec_path))
    elif spec.endswith(':'):
      spec_path = spec[:-len(':')]
      return SiblingAddresses(self._normalize_spec_path(spec_path))
    else:
      spec_parts = spec.rsplit(':', 1)
      spec_path = self._normalize_spec_path(spec_parts[0]) 
      name = spec_parts[1] if len(spec_parts) > 1 else os.path.basename(spec_path)
      return SingleAddress(spec_path, name)
