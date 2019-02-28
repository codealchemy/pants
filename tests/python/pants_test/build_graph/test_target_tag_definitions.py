# coding=utf-8
# Copyright 2019 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import absolute_import, division, print_function, unicode_literals

import json

from pants.build_graph.target_tag_definitions import TargetTagDefinitions
from pants.task.task import Task
from pants.util.contextutil import temporary_file
from pants_test.task_test_base import TaskTestBase


class TestTargetTagDefinitions(TaskTestBase):
  
  class DummyTask(Task):
    options_scope = 'dummy'

    def execute(self): pass

  @classmethod
  def task_type(cls):
    return cls.DummyTask

  def test_target_tags_match_those_configured(self):
      with temporary_file(binary_mode=False) as fp:
        json.dump({
          'tag_targets_mappings': {
            'tag1': ['target3'],
            'tag2': ['target3', 'target2']
          }
        }, fp)
        fp.flush()

        self.context(for_subsystems=[TargetTagDefinitions], options={
          TargetTagDefinitions.options_scope: {
            'source_json': fp.name
          }
        })

        target_tag_definitions = TargetTagDefinitions.global_instance()
        target1_tags = target_tag_definitions.tags_for('target1')
        target2_tags = target_tag_definitions.tags_for('target2')
        target3_tags = target_tag_definitions.tags_for('target3')

        self.assertEqual([], target1_tags)
        self.assertEqual(['tag2'], target2_tags)
        self.assertEqual(['tag1', 'tag2'], target3_tags)
