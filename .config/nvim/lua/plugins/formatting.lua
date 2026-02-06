return {
	{
		"stevearc/conform.nvim",
		event = { "BufReadPre", "BufNewFile" },
		config = function()
			local conform = require("conform")
			conform.setup({
				formatters_by_ft = {
					lua = { "stylua" },
					cpp = { "clang-format" },
					-- cmake = { "cmakelang" },
					python = { "ruff_format", "ruff_fix", "ruff_organize_imports" },
					latex = { "tex-fmt" },
					html = { "prettier" },
					css = { "prettier" },
					javascript = { "prettier" },
					json = { "prettier" },
					toml = { "taplo" },
				},

				format_on_save = function(bufnr)
					if vim.g.disable_autoformat or vim.b[bufnr].disable_autoformat then
						return
					end

					local bufname = vim.api.nvim_buf_get_name(bufnr)
					if bufname:match("/vm_share/") then
						return
					end

					return { lsp_fallback = true, async = false, timeout_ms = 1000 }
				end,
			})

			vim.api.nvim_create_user_command("FormatDisable", function(args)
				if args.bang then
					-- FormatDisable! will disable formatting just for this buffer
					vim.b.disable_autoformat = true
				else
					vim.g.disable_autoformat = true
				end
			end, {
				desc = "Disable autoformat-on-save",
				bang = true,
			})
			vim.api.nvim_create_user_command("FormatEnable", function()
				vim.b.disable_autoformat = false
				vim.g.disable_autoformat = false
			end, {
				desc = "Re-enable autoformat-on-save",
			})

			vim.keymap.set("", "<leader>f", function()
				require("conform").format({ lsp_fallback = true, async = false, timeout_ms = 1000 }, function(err)
					if not err then
						local mode = vim.api.nvim_get_mode().mode
						if vim.startswith(string.lower(mode), "v") then
							vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("<Esc>", true, false, true), "n", true)
						end
					end
				end)
			end, { desc = "Format code" })
		end,
	},
}
