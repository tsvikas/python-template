#!/usr/bin/env just --justfile
default:
  @just --list

test:
  rm -rf .ctt
  uvx --from copier-template-tester --with copier_templates_extensions ctt
