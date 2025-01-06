#!/usr/bin/env python3
from pathlib import Path


def get_stages(lines):
    stage_name = None
    stage_data = []
    for line in lines:
        if not line.startswith("  "):
            raise RuntimeError("stage_data contains other sections")
        if len(line.lstrip(" ")) + 2 == len(line):
            # new stage
            if stage_name is not None:
                yield stage_name, stage_data
            stage_name = line[2:-1]
            stage_data = [line]
        else:
            stage_data.append(line)
    yield stage_name, stage_data


def fix_lock_file(yaml_file, lock_file, keep_urban_stages=False):
    # get sorted stages
    yaml_data = yaml_file.read_text().splitlines()
    yaml_prefix_lines_num = yaml_data.index("stages:") + 1
    assert yaml_prefix_lines_num == 1
    _yaml_header, yaml_stages = (
        yaml_data[:yaml_prefix_lines_num],
        yaml_data[yaml_prefix_lines_num:],
    )
    sorted_stages = [stage_name for stage_name, stage_data in get_stages(yaml_stages)]
    # get locked stage data
    lock_data = lock_file.read_text().splitlines()
    lock_prefix_lines_num = lock_data.index("stages:") + 1
    assert lock_prefix_lines_num == 2  # noqa: PLR2004
    lock_header, lock_stages = (
        lock_data[:lock_prefix_lines_num],
        lock_data[lock_prefix_lines_num:],
    )
    stages_dict = dict(get_stages(lock_stages))
    # rearrange
    new_stages_dict = {k: stages_dict.pop(k) for k in sorted_stages if k in stages_dict}
    if keep_urban_stages:
        new_stages_dict.update(stages_dict)
    # transform to lines
    output_lines = lock_header[:]
    for stage_lines in new_stages_dict.values():
        output_lines.extend(stage_lines)
    # write to file
    lock_file.write_text("\n".join(output_lines) + "\n")


def main():
    base_dir = Path().resolve()
    while not base_dir.joinpath("dvc.lock").exists():
        if base_dir == Path("/"):
            raise RuntimeError("dvc.lock file not found")
        base_dir = base_dir.parent
    yaml_file = base_dir / "dvc.yaml"
    assert yaml_file.exists()
    lock_file = base_dir / "dvc.lock"
    assert lock_file.exists()
    fix_lock_file(yaml_file, lock_file)


if __name__ == "__main__":
    main()
