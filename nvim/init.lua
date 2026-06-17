-- 1. Ensure all NVMe directories exist firs0
require("util.paths").ensure()

-- 2. Core options (storage paths must be set before plugins load)
require("core.options")

-- 3. Keymaps
require("core.keymaps")

-- 4. Autocommands
require("core.autocmds")

-- 5. Plugin manager (loads all plugins/)
require("core.lazy")
