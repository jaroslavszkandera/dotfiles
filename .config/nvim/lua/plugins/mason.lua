return {
	"mason-org/mason.nvim",
	dependencies = {
		"mason-org/mason-lspconfig.nvim",
		"WhoIsSethDaniel/mason-tool-installer.nvim",
	},
	config = function()
		local mason = require("mason")
		local mason_lspconfig = require("mason-lspconfig")
		local mason_tool_installer = require("mason-tool-installer")

		mason.setup({
			log_level = vim.log.levels.INFO,
		})

		mason_lspconfig.setup({
			ensure_installed = {
				"ruff",
				"clangd",
				"neocmake",
				"bashls",
				"rust_analyzer",
				"lua_ls",
			},
		})

		mason_tool_installer.setup({
			ensure_installed = {
				"stylua",
				"clang-format",
				"ruff",
			},
		})
	end,
}
