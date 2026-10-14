return {
	{
		"folke/snacks.nvim",
		priority = 1000,
		lazy = false,
		opts = {
			bigfile = { enabled = true },
			dashboard = { enabled = true },
			explorer = { enabled = true },
			-- indent = { enabled = true },
			input = { enabled = true },
			picker = {
				enabled = true,
				---@class snacks.picker.matcher.Config
				matcher = {
					fuzzy = true, -- use fuzzy matching
					smartcase = true, -- use smartcase
					ignorecase = true, -- use ignorecase
					sort_empty = false, -- sort results when the search string is empty
					filename_bonus = true, -- give bonus for matching file names (last part of the path)
					file_pos = true, -- support patterns like `file:line:col` and `file:line`
					-- the bonusses below, possibly require string concatenation and path normalization,
					-- so this can have a performance impact for large lists and increase memory usage
					cwd_bonus = false, -- give bonus for matching files in the cwd
					frecency = true, -- frecency bonus
					history_bonus = false, -- give more weight to chronological order
				},
			},
			quickfile = { enabled = true },
			-- scope = { enabled = true },
			statuscolumn = { enabled = true },
			-- words = { enabled = true },
		},
		keys = {
			{
				"<leader>e",
				function()
					Snacks.explorer()
				end,
				desc = "Explorer",
			},
			{
				"<leader>ff",
				function()
					Snacks.picker.files()
				end,
				desc = "Find Files",
			},
			{
				"<leader>fg",
				function()
					Snacks.picker.grep()
				end,
				desc = "Grep",
			},
			{
				"<leader>fb",
				function()
					Snacks.picker.buffers()
				end,
				desc = "Buffers",
			},
			{
				"<leader>fh",
				function()
					Snacks.picker.help()
				end,
				desc = "Help",
			},
			{
				"<leader>fk",
				function()
					Snacks.picker.keymaps()
				end,
				desc = "Keymaps",
			},
			{
				"<leader>fr",
				function()
					Snacks.picker.recent()
				end,
				desc = "Recent Files",
			},
			{
				"<leader>fc",
				function()
					Snacks.picker.commands()
				end,
				desc = "Commands",
			},
			{
				"<leader>fs",
				function()
					Snacks.picker.lsp_symbols()
				end,
				desc = "LSP Symbols",
			},
			{
				"<leader>fd",
				function()
					Snacks.picker.diagnostics()
				end,
				desc = "Diagnostics",
			},
			{
				"<leader>fn",
				function()
					Snacks.picker.notifications()
				end,
				desc = "Notifications",
			},
			{
				"gd",
				function()
					Snacks.picker.lsp_definitions()
				end,
				desc = "Goto Definition",
			},
			{
				"gr",
				function()
					Snacks.picker.lsp_references()
				end,
				desc = "References",
			},
			{
				"gi",
				function()
					Snacks.picker.lsp_implementations()
				end,
				desc = "Implementations",
			},
			{
				"gt",
				function()
					Snacks.picker.lsp_type_definitions()
				end,
				desc = "Type Definitions",
			},
			{
				"<leader>ss",
				function()
					Snacks.picker.lsp_workspace_symbols()
				end,
				desc = "Workspace Symbols",
			},
		},
	},
	{
		"folke/which-key.nvim",
		event = "VeryLazy",
		opts = {},
		keys = {
			{
				"<leader>?",
				function()
					require("which-key").show({ global = false })
				end,
				desc = "Buffer Keymaps",
			},
			{
				"<leader>w?",
				function()
					require("which-key").show({ global = true })
				end,
				desc = "All Keymaps",
			},
		},
	},
}
