-- line numbers and relative line numbers
vim.opt.nu = true
vim.opt.relativenumber = true

-- indenting
vim.opt.tabstop = 2
vim.opt.softtabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true

-- automatically wrap text to another line and smart wrap
vim.opt.wrap = true
vim.opt.linebreak = true

-- undotree
-- vim.opt.undodir = os.getenv("HOME") .. "/.vim/undodir"
-- vim.opt.undofile = true

-- search settings
vim.opt.ignorecase = true
vim.opt.smartcase = true

-- highlighting incremental search
vim.opt.hlsearch = true
vim.opt.incsearch = true

-- good colors
vim.opt.termguicolors = true

-- TODO: fix first <Ctrl+d> screen tear
-- never have less than 8 line from bottom/top
vim.opt.scrolloff = 8
vim.opt.signcolumn = "yes"
vim.opt.isfname:append("@-@")

-- fast update time
vim.opt.updatetime = 50

-- enable system clipboard
vim.o.clipboard = "unnamedplus"

-- save undo history
vim.opt.undofile = true
