return {
  {
    "nvim-treesitter/nvim-treesitter",
    event = {"BufReadPost", "BufNewFile"},
    build = ":TSUpdate",
    dependencies = {
      "windwp/nvim-ts-autotag",
    },
    config = function()
      require("nvim-treesitter.configs").setup({
        highlight = { enable = true },
        indent = { enable = true },
        autotag = { enable = true },
        ensure_installed = {
          "lua",
          "c",
          "cpp",
          "python",
          "rust",
          "go",
          "bash",
          "gitignore",
          "markdown",
          "markdown_inline",
          "json",
          "vim",
          "vimdoc",
        },
        incremental_selection = {
          enable = true,
          keymaps = {
            init_selection = "<C-space>",
            node_incremental = "<C-space>",
            scope_incremental = false,
            node_decremental = "<bs>",
          },
        },
      })
    end,
  },
}
