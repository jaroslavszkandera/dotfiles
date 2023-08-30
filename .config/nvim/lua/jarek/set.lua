-- fat cursor
-- vim.opt.guicursor = ""

-- line numbers and relative line numbers
vim.opt.nu = true
vim.opt.relativenumber = true

-- indenting
vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true

vim.opt.wrap = true

-- smart wrap
vim.opt.wrap = false

-- forbid backups
vim.opt.swapfile = false
vim.opt.backup = false
-- undotree for days
vim.opt.undodir = os.getenv("HOME") .. "/.vim/undodir"
vim.opt.undofile = true

-- non-highlighting incremental search
vim.opt.hlsearch = true
vim.opt.incsearch = true

vim.opt.termguicolors = true

-- never have less than 8 line from bottom/top
vim.opt.scrolloff = 8
vim.opt.signcolumn = "yes"
vim.opt.isfname:append("@-@")

-- fast update time
vim.opt.updatetime = 50

-- vim.opt.colorcolumn = "80"

vim.o.clipboard = "unnamedplus"
