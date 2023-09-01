#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pytest import MonkeyPatch

from cmk.gui.plugins.wato.utils.main_menu import MainModuleTopicExporter
from cmk.gui.watolib import main_menu
from cmk.gui.watolib.main_menu import ABCMainModule, MainModuleRegistry


def test_register_modules(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(main_menu, "main_module_registry", MainModuleRegistry())
    module = main_menu.WatoModule(
        mode_or_url="dang",
        description="descr",
        permission="icons",
        title="Custom DING",
        sort_index=100,
        icon="icons",
    )
    main_menu.register_modules(module)

    modules = list(main_menu.main_module_registry.values())  # type: ignore[attr-defined]
    assert len(modules) == 1
    registered = modules[0]()
    assert isinstance(registered, ABCMainModule)
    assert registered.mode_or_url == "dang"
    assert registered.description == "descr"
    assert registered.permission == "icons"
    assert registered.title == "Custom DING"
    assert registered.sort_index == 100
    assert registered.icon == "icons"
    assert registered.is_show_more is False
    assert registered.topic == MainModuleTopicExporter
