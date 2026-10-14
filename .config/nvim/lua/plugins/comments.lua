vim.filetype.add({ extension = { slint = "slint" } })

vim.api.nvim_create_autocmd("FileType", {
	pattern = "slint",
	callback = function()
		vim.bo.commentstring = "// %s"
	end,
	desc = "Use // comments for slint (fixes [Comment.nvim] nil)",
})

return {
	{
		"numToStr/Comment.nvim",
		opts = {
			pre_hook = function()
				-- workaround for slint files
				if vim.bo.filetype == "slint" then
					return "//%s"
				end
			end,
		},
	},
	{
		"folke/todo-comments.nvim",
		event = "VimEnter",
		dependencies = { "nvim-lua/plenary.nvim" },
		opts = { signs = false },
	},
}
