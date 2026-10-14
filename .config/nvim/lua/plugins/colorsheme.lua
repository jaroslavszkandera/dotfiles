return {
	{
		"cocopon/iceberg.vim",
		lazy = false,
		priority = 1000,
		config = function()
			vim.cmd.colorscheme("iceberg")
			vim.api.nvim_set_hl(0, "NonText", { fg = "#6b7089" })
		end,
	},
}
