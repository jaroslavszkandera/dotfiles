return {
	{
		"folke/trouble.nvim",
		cmd = "Trouble",
		opts = {},
		keys = {
			{ "<leader>xx", "<cmd>Trouble diagnostics toggle<CR>", desc = "Diagnostics (Trouble)" },
			{ "<leader>xX", "<cmd>Trouble diagnostics toggle filter.buf=0<CR>", desc = "Buffer Diagnostics" },
			{ "<leader>cs", "<cmd>Trouble symbols toggle<CR>", desc = "Symbols" },
			{ "<leader>cl", "<cmd>Trouble lsp toggle<CR>", desc = "LSP Definitions/References" },
			{ "<leader>xL", "<cmd>Trouble loclist toggle<CR>", desc = "Location List" },
			{ "<leader>xQ", "<cmd>Trouble qflist toggle<CR>", desc = "Quickfix List" },
		},
	},
}
