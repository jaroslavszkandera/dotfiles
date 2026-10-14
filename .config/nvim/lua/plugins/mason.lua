return {
	"mason-org/mason.nvim",
	dependencies = {
		"mason-org/mason-lspconfig.nvim",
		"WhoIsSethDaniel/mason-tool-installer.nvim",
	},
	config = function()
		local mason = require("mason")
		local mason_lspconfig
		local mason_tool_installer

		mason.setup({
			log_level = vim.log.levels.INFO,
			pip = {
				upgrade_pip = true,
				install_args = { "--no-cache-dir" },
			},
		})

		mason_lspconfig = require("mason-lspconfig")
		mason_tool_installer = require("mason-tool-installer")

		mason_lspconfig.setup({
			ensure_installed = {
				"ruff",
				"clangd",
				"neocmake",
				"bashls",
				"rust_analyzer",
				"lua_ls",
				"basedpyright",
				"taplo",
				"ltex_plus",
			},
			automatic_enable = true,
		})

		mason_tool_installer.setup({
			ensure_installed = {
				"stylua",
				"clang-format",
				"cpplint",
				"taplo",
				"alejandra",
				"codelldb",
			},
		})
	end,
}
