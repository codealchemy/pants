# coding=utf-8
# Copyright 2019 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging

from pants.base.build_environment import get_buildroot
from pants.subsystem.subsystem import Subsystem
from pants.util.dirutil import maybe_read_file
from pants.util.memo import memoized_property


logger = logging.getLogger(__name__)
  

class TargetTagDefinitions(Subsystem):
  """Tags to be applied to targets defined in a single JSON source file.

  :API: public
  """

  DEFAULT_TAG_DEFINITON_FILE = "{}/target_tag_definitions.json".format(get_buildroot())

  options_scope = 'target-tag-definitions'

  @classmethod
  def register_options(cls, register):
    super(TargetTagDefinitions, cls).register_options(register)

    register('--source-json', type=str,
             default=cls.DEFAULT_TAG_DEFINITON_FILE, fingerprint=True,
             help='Source JSON file with tag definitions for targets.')

  def tags_for(self, target_name):
    return self.parsed_tag_definitions.get(target_name, [])

  @memoized_property
  def parsed_tag_definitions(self):
    tag_definitions = maybe_read_file(self.get_options().source_json, binary_mode=False)

    if tag_definitions:
      parsed_json = json.loads(tag_definitions)
      mappings = parsed_json.get("tag_targets_mappings", {})
      return self._invert_tag_targets_mappings(mappings)
    else:
      return {}

  def _invert_tag_targets_mappings(self, parsed_json):
    result = {}
    for tag, targets in parsed_json.items():
      for target in targets:
        target_tags = result.setdefault(target, [])
        target_tags.append(tag)
    return result
