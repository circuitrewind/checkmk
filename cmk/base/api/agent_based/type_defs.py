#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
"""Type definitions

Some of these are exposed in the API, some are not.
"""

from collections.abc import Callable, Generator, Sequence
from typing import Any, Literal, NamedTuple, Protocol

from cmk.utils.check_utils import ParametersTypeAlias
from cmk.utils.rulesets import RuleSetName
from cmk.utils.sectionname import SectionName

from cmk.snmplib import SNMPDetectBaseType

from cmk.checkengine.sectionparser import ParsedSectionName

from cmk.agent_based.v1 import HostLabel

RuleSetTypeName = Literal["merged", "all"]

StringTable = list[list[str]]
StringByteTable = list[list[str | list[int]]]

AgentParseFunction = Callable[[StringTable], Any]

HostLabelGenerator = Generator[HostLabel, None, None]
HostLabelFunction = Callable[..., HostLabelGenerator]

SNMPParseFunction = Callable[[list[StringTable]], Any] | Callable[[list[StringByteTable]], Any]

SimpleSNMPParseFunction = Callable[[StringTable], Any] | Callable[[StringByteTable], Any]


class AgentSectionPlugin(NamedTuple):
    name: SectionName
    parsed_section_name: ParsedSectionName
    parse_function: AgentParseFunction
    host_label_function: HostLabelFunction
    host_label_default_parameters: ParametersTypeAlias | None
    host_label_ruleset_name: RuleSetName | None
    host_label_ruleset_type: RuleSetTypeName
    supersedes: set[SectionName]
    full_module: str | None  # not available for auto migrated plugins.


class _OIDSpecLike(Protocol):
    @property
    def column(self) -> int | str:
        ...

    @property
    def encoding(self) -> Literal["string", "binary"]:
        ...

    @property
    def save_to_cache(self) -> bool:
        ...


class _SNMPTreeLike(Protocol):
    @property
    def base(self) -> str:
        ...

    @property
    def oids(self) -> Sequence[_OIDSpecLike]:
        ...


class SNMPSectionPlugin(NamedTuple):
    name: SectionName
    parsed_section_name: ParsedSectionName
    parse_function: SNMPParseFunction
    host_label_function: HostLabelFunction
    host_label_default_parameters: ParametersTypeAlias | None
    host_label_ruleset_name: RuleSetName | None
    host_label_ruleset_type: RuleSetTypeName
    detect_spec: SNMPDetectBaseType
    trees: Sequence[_SNMPTreeLike]
    supersedes: set[SectionName]
    full_module: str | None  # not available for auto migrated plugins.


SectionPlugin = AgentSectionPlugin | SNMPSectionPlugin
