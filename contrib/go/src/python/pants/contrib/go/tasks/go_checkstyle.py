# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.base.exceptions import TaskError
from pants.task.lint_task_mixin import LintTaskMixin

from pants.contrib.go.tasks.go_fmt_task_base import GoFmtTaskBase


class GoCheckstyle(LintTaskMixin, GoFmtTaskBase):
  """Checks Go code matches gofmt style."""

  @property
  def skip_execution(self):
    return super()._resolve_conflicting_skip(old_scope="lint-go")

  def execute(self):
    with self.go_fmt_invalid_targets(['-d']) as output:
      if output:
        self.context.log.error(output)
        raise TaskError('Found style errors. Use `./pants fmt` to fix.')
