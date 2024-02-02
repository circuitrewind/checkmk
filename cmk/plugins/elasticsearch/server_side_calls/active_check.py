#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Iterator
from typing import Literal

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
    HostConfig,
    parse_secret,
    replace_macros,
    Secret,
)


class Params(BaseModel):
    svc_item: str
    hostname: str | None = None
    protocol: Literal["http", "https"] | None = None
    user: str | None = None
    password: tuple[Literal["password", "store"], str] | None = None
    port: int | None = None
    index: list[str] | None = None
    pattern: str
    fieldname: list[str] | None = None
    timerange: int
    count: tuple[int, int] | None = None


def commands_function(
    params: Params, host_config: HostConfig, _http_proxies: object
) -> Iterator[ActiveCheckCommand]:
    args: list[str | Secret] = ["-q", params.pattern, "-t", str(params.timerange)]

    if params.protocol is not None:
        args += ["-P", params.protocol]
    if params.user is not None:
        args += ["-u", params.user]
    if params.password is not None:
        args += ["-s", parse_secret(params.password)]
    if params.port is not None:
        args += ["-p", str(params.port)]
    if params.index:
        args += ["-i", " ".join(params.index)]
    if params.fieldname is not None:
        args += ["-f", " ".join(params.fieldname)]
    if params.count is not None:
        warn, crit = params.count
        args += ["--warn=%d" % warn, "--crit=%d" % crit]

    if params.hostname is not None:
        args += ["-H", replace_macros(params.hostname, host_config.macros)]
    elif host_config.resolved_address:
        args += ["-H", host_config.resolved_address]
    else:
        raise ValueError("No IP address available")

    item = replace_macros(params.svc_item, host_config.macros)
    yield ActiveCheckCommand(
        service_description=f"Elasticsearch Query {item}", command_arguments=args
    )


active_check_config = ActiveCheckConfig(
    name="elasticsearch_query",
    parameter_parser=Params.model_validate,
    commands_function=commands_function,
)
