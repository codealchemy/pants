# Copyright 2019 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

target(
  name = 'all_directories',
  dependencies = [
    ':grpcio_directory',
    ':hello_directory',
    ':pants_publish_plugin_directory',
    ':tensorflow_custom_op_directory',
  ],
)

page(
  name='readme',
  source='README.md',
  links=[
    ':3rdparty_py',
    'src/docs:first_concepts',
  ]
)

page(
  name='3rdparty_py',
  source='3rdparty_py.md',
  links=[
    'src/docs:3rdparty',
  ]
)

files(
  name='grpcio_directory',
  sources=rglobs('grpcio/*'),
  dependencies = [
    'examples/3rdparty:python_directory',
    'examples/src/protobuf/org/pantsbuild/example:grpcio_directory',
  ],
)

files(
  name='hello_directory',
  sources=rglobs('hello/*'),
)

files(
  name='pants_publish_plugin_directory',
  sources=rglobs('pants_publish_plugin/*'),
)

files(
  name='tensorflow_custom_op_directory',
  sources=rglobs('tensorflow_custom_op/*'),
  dependencies = [
    'examples/3rdparty:python_directory',
  ],
)
