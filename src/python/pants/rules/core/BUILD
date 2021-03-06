# Copyright 2018 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  dependencies = [
    '3rdparty/python:dataclasses',
    'src/python/pants:version',
    'src/python/pants/base:build_root',
    'src/python/pants/base:exiter',
    'src/python/pants/build_graph',
    'src/python/pants/engine:goal',
    'src/python/pants/engine:rules',
    'src/python/pants/engine:interactive_runner',
    'src/python/pants/engine:selectors',
    'src/python/pants/engine:addressable',
    'src/python/pants/engine:console',
    'src/python/pants/engine/legacy:graph',
    'src/python/pants/goal',
    'src/python/pants/source',
    'src/python/pants/util:collections',
  ],
  tags = {"type_checked"},
)

python_tests(
  name = "tests",
  sources=globs('*_test.py', exclude=[globs('*_integration_test.py')]),
  dependencies = [
    ':core',
    'src/python/pants:version',
    'src/python/pants/backend/codegen/thrift/java',
    'src/python/pants/backend/jvm/targets:all',
    'src/python/pants/backend/python/targets',
    'src/python/pants/build_graph',
    'src/python/pants/engine:fs',
    'src/python/pants/engine/legacy:graph',
    'src/python/pants/engine/legacy:structs',
    'src/python/pants/testutil:test_base',
    'src/python/pants/testutil:console_rule_test_base',
    'src/python/pants/testutil/engine:util',
    'src/python/pants/testutil/subsystem',
  ],
  tags = {"partially_type_checked"},
)

python_tests(
  name='integration',
  sources=globs('*_integration_test.py'),
  dependencies=[
    'src/python/pants/testutil:int-test',
    'examples/src/java/org/pantsbuild/example:hello_directory',
    'examples/src/scala/org/pantsbuild/example:hello_directory',
    'examples/src/resources/org/pantsbuild/example:hello_directory',
  ],
  tags = {'integration', 'partially_type_checked'},
)
