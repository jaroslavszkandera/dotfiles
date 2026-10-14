return {
	{
		"neovim/nvim-lspconfig",
		event = { "BufReadPre", "BufNewFile" },
		dependencies = {
			"hrsh7th/cmp-nvim-lsp",
			{ "antosha417/nvim-lsp-file-operations", config = true },
		},
		config = function()
			local lspconfig = require("lspconfig")
			local cmp_nvim_lsp = require("cmp_nvim_lsp")
			local keymap = vim.keymap
			local capabilities = cmp_nvim_lsp.default_capabilities()

			vim.lsp.config("lua_ls", {
				settings = {
					Lua = {
						runtime = { version = "LuaJIT" },
						diagnostics = { globals = { "vim", "require" } },
						workspace = { checkThirdParty = false },
						telemetry = { enable = false },
					},
				},
			})

			vim.lsp.config("basedpyright", {
				capabilities = capabilities,
				settings = {
					basedpyright = {
						analysis = {
							typeCheckingMode = "basic",
							diagnosticMode = "workspace",
							inlayHints = { variableTypes = true, callArgumentNames = true },
							autoImportCompletions = true,
						},
					},
				},
				on_attach = function(client, bufnr)
					client.server_capabilities.semanticTokensProvider = nil
					client.server_capabilities.documentFormattingProvider = false
				end,
			})

			vim.lsp.config("ruff", {
				capabilities = capabilities,
				on_attach = function(client)
					client.server_capabilities.hoverProvider = true
				end,
			})

			vim.lsp.config("rust_analyzer", {
				capabilities = capabilities,
				settings = {
					["rust-analyzer"] = {
						cargo = { allFeatures = true, loadOutDirsFromCheck = true },
						procMacro = { enable = true },
						checkOnSave = { enable = true },
						inlayHints = {
							bindingModeHints = { enable = true },
							chainingHints = { enable = true },
							closureReturnTypeHints = { enable = true },
							lifetimeElisionHints = { enable = "always" },
							renderColons = true,
						},
						diagnostics = {
							enable = true,
							disabled = { "unresolved-proc-macro" },
							enableExperimental = true,
						},
						files = { excludeDirs = { ".git", "target", "node_modules" } },
					},
				},
			})

			vim.lsp.config("clangd", {
				capabilities = capabilities,
				cmd = {
					"clangd",
					"--background-index",
					"--clang-tidy",
					"--header-insertion=iwyu",
					"--completion-style=detailed",
					"--function-arg-placeholders",
					"--fallback-style=llvm",
				},
				init_options = {
					usePlaceholders = true,
					completeUnimported = true,
					clangdFileStatus = true,
				},
			})

			vim.lsp.config("bashls", { capabilities = capabilities })
			vim.lsp.config("neocmake", { capabilities = capabilities })
			vim.lsp.config("taplo", { capabilities = capabilities })
			vim.lsp.config("ltex_plus", {
				capabilities = capabilities,
				filetypes = { "tex", "bib", "markdown" },
				settings = {
					ltex = {
						language = "en-US",
						latex = { environments = { itemize = "ignore", enumerate = "ignore" } },
						disabledRules = { ["en-US"] = { "WHITESPACE_RULE", "EN_QUOTES" } },
						dictionary = {
							["en-US"] = {
								"keymaps",
								"keymap",
								"nvim",
								"lazy",
								"lsp",
								"treesitter",
								"conform",
								"harpoon",
								"telescope",
							},
						},
						hiddenFalsePositives = {},
					},
				},
				on_attach = function(client, bufnr)
					vim.opt_local.spell = true
				end,
			})

			vim.lsp.enable("rust_analyzer")
			vim.lsp.enable("ltex_plus")

			vim.api.nvim_create_autocmd("LspAttach", {
				group = vim.api.nvim_create_augroup("UserLspConfig", {}),
				callback = function(ev)
					local opts = { buffer = ev.buf, silent = true }

					opts.desc = "Show LSP references"
					keymap.set("n", "gR", function()
						Snacks.picker.lsp_references()
					end, opts)

					opts.desc = "Go to declaration"
					keymap.set("n", "gD", vim.lsp.buf.declaration, opts)

					opts.desc = "Show LSP definitions"
					keymap.set("n", "gd", function()
						Snacks.picker.lsp_definitions()
					end, opts)

					opts.desc = "Show LSP implementations"
					keymap.set("n", "gi", function()
						Snacks.picker.lsp_implementations()
					end, opts)

					opts.desc = "Show LSP type definitions"
					keymap.set("n", "gt", function()
						Snacks.picker.lsp_type_definitions()
					end, opts)

					opts.desc = "Fix diagnostic"
					keymap.set("n", "<leader>ca", function()
						vim.lsp.buf.code_action({ apply = true })
					end, opts)

					opts.desc = "Smart rename"
					keymap.set("n", "<leader>rn", vim.lsp.buf.rename, opts)

					opts.desc = "Show buffer diagnostics"
					keymap.set("n", "<leader>D", function()
						Snacks.picker.diagnostics({ bufnr = 0 })
					end, opts)

					opts.desc = "Show line diagnostics"
					keymap.set("n", "<leader>d", vim.diagnostic.open_float, opts)

					opts.desc = "Go to previous diagnostic"
					keymap.set("n", "[d", function()
						vim.diagnostic.jump({ count = -1 })
					end, opts)

					opts.desc = "Go to next diagnostic"
					keymap.set("n", "]d", function()
						vim.diagnostic.jump({ count = 1 })
					end, opts)

					opts.desc = "Show documentation for what is under cursor"
					keymap.set("n", "K", vim.lsp.buf.hover, opts)

					opts.desc = "Restart LSP"
					keymap.set("n", "<leader>rs", ":LspRestart<CR>", opts)
				end,
			})

			vim.diagnostic.config({
				virtual_text = {
					source = "always",
					format = function(diagnostic)
						return string.format("%s %s", diagnostic.severity, diagnostic.message)
					end,
				},
				signs = true,
				update_in_insert = false,
				severity_sort = true,
				float = {
					source = "always",
					header = "",
					prefix = "",
				},
			})
		end,
	},
	{
		"folke/lazydev.nvim",
		ft = "lua",
		opts = {
			library = { { path = "${3rd}/luv/library", words = { "vim%.uv" } } },
		},
	},
}
