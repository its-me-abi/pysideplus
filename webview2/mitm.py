import asyncio
from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

import logging
logging.getLogger("mitmdump").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)



class MitmProxyManager:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.options = Options(listen_host=self.host, listen_port=self.port)
        self.dump_master = None
        self.addons = []

    def add_addon(self, addon):
        """Add custom addons to Mitmproxy."""
        self.addons.append(addon)  # Store the addon for tracking
        if self.dump_master:  # Ensure DumpMaster exists before adding addons
            self.dump_master.addons.add(addon)

    def start(self):
        """Start Mitmproxy with an event loop."""

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._run_mitmproxy())

    async def _run_mitmproxy(self):
        """Async method to run Mitmproxy."""
        self.dump_master = DumpMaster(self.options)
        for addon in self.addons:
            self.dump_master.addons.add(addon)
        try:
            await self.dump_master.run()
        except KeyboardInterrupt:
            self.dump_master.shutdown()

class CustomAddon:
    def request(self, flow):
        print("### request recived ")

    def response(self, flow):
        """Customize responses with this addon."""
        print("### responce recived ")

# Main script
if __name__ == "__main__":
    manager = MitmProxyManager(host="127.0.0.1", port=8080)

    # Add your custom addons
    custom_addon = CustomAddon()
    manager.add_addon(custom_addon)

    # Start Mitmproxy
    manager.start()
