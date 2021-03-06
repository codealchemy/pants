# Copyright 2019 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from dataclasses import dataclass
from pathlib import Path

from pants.base.build_root import BuildRoot
from pants.engine.rules import rule
from pants.fs.fs import is_child_of
from pants.option.options_bootstrapper import OptionsBootstrapper


class InvalidDistDir(Exception):
  pass


@dataclass(frozen=True)
class DistDir:
  """The directory to which we write distributable files."""
  relpath: Path


@rule
async def get_distdir(options_bootstrapper: OptionsBootstrapper, buildroot: BuildRoot) -> DistDir:
  global_options = options_bootstrapper.bootstrap_options.for_global_scope()
  return validate_distdir(Path(global_options.pants_distdir), buildroot.pathlib_path)


def validate_distdir(distdir: Path, buildroot: Path) -> DistDir:
  if not is_child_of(distdir, buildroot):
    raise InvalidDistDir(
      f"When set to an absolute path, `--pants-distdir` must be relative to the build root."
      f"You set it to {distdir}. Instead, use a relative path or an absolute path relative "
      f"to the build root."
    )
  relpath = distdir.relative_to(buildroot) if distdir.is_absolute() else distdir
  return DistDir(relpath)


def rules():
  return [
    get_distdir,
  ]
