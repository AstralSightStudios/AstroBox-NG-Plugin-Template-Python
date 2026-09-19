"""AstroBox 插件入口。

componentize-py 按 WIT 里的**导出接口名**在本模块里找实现类，所以这两个类必须
叫 `Lifecycle` 和 `Event`，不能改名。
"""

import wit_world.exports as exports
from wit_world.exports import event as event_types
from wit_world.imports import os as host_os
from wit_world.imports import ui


class Lifecycle(exports.Lifecycle):
    async def on_load(self) -> None:
        # Level 4 的 on-load 是 async func，可以直接 await 宿主接口，
        # 不需要 Level 2/3 那种 block_on 变通。
        arch = await host_os.arch()
        platform = await host_os.platform()
        print(f"Hello AstroBox! running on {platform}/{arch}")


class Event(exports.Event):
    async def on_event(self, event_type: event_types.EventType, event_payload: str) -> str:
        print(f"event: {event_type} {event_payload}")
        return ""

    async def on_ui_event(self, event_id: str, event: ui.Event, event_payload: str) -> str:
        print(f"ui event: {event_id} {event} {event_payload}")
        return ""

    async def on_ui_render(self, element_id: str) -> None:
        size = await ui.get_render_size()
        root = ui.Element(ui.ElementType.DIV, None).flex().flex_direction(
            ui.FlexDirection.COLUMN
        )
        title = ui.Element(ui.ElementType.P, f"Hello from Python ({size.width}x{size.height})")
        ui.render(element_id, root.child(title))

    async def on_card_render(self, card_id: str) -> None:
        ui.render_to_text_card(card_id, "Hello from Python")
