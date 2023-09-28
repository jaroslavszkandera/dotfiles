-- line numbers and relative line numbers
vim.opt.nu = true
vim.opt.relativenumber = true

-- indenting
vim.opt.tabstop = 2
vim.opt.softtabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true

-- automatically wrap text to another line
vim.opt.wrap = true

-- smart wrap
vim.opt.wrap = false

-- forbid backups
vim.opt.swapfile = false
vim.opt.backup = false

-- undotree for days
vim.opt.undodir = os.getenv("HOME") .. "/.vim/undodir"
vim.opt.undofile = true

-- highlighting incremental search
vim.opt.hlsearch = true
vim.opt.incsearch = true

-- good colors
vim.opt.termguicolors = true

-- never have less than 8 line from bottom/top
vim.opt.scrolloff = 8
vim.opt.signcolumn = "yes"
vim.opt.isfname:append("@-@")

-- fast update time
vim.opt.updatetime = 50

-- enable system clipboard
vim.o.clipboard = "unnamedplus"
