#!/usr/bin/env just --justfile
default:
  @just --list

test:
  rm -rf .ctt
  uvx --from git+https://github.com/tsvikas/copier-template-tester@feat/add-tasks --with copier_templates_extensions ctt
