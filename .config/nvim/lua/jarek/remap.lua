vim.g.mapleader = " "
-- while in normal mode, press leader pv it will execute this command
vim.keymap.set("n", "<leader>e", vim.cmd.Ex)

vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

vim.keymap.set("n", "J", "mzJ`z")
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")
vim.keymap.set("n", "n", "nzzzv")
vim.keymap.set("n", "N", "Nzzzv")

-- greatest remap ever
vim.keymap.set("x", "<leader>p", [["_dP]])

-- next greatest remap ever : asbjornHaland
vim.keymap.set({ "n", "v" }, "<leader>y", [["+y]])
vim.keymap.set("n", "<leader>Y", [["+Y]])

vim.keymap.set({ "n", "v" }, "<leader>d", [["_d]])

-- This is going to get me cancelled
vim.keymap.set("i", "<C-c>", "<Esc>")

vim.keymap.set("n", "Q", "<nop>")
vim.keymap.set("n", "<C-f>", "<cmd>silent !tmux neww tmux-sessionizer<CR>")
vim.keymap.set("n", "<leader>f", vim.lsp.buf.format)

-- vim.keymap.set("n", "<C-k>", "<cmd>cnext<CR>zz")
-- vim.keymap.set("n", "<C-j>", "<cmd>cprev<CR>zz")
vim.keymap.set("n", "<leader>k", "<cmd>lnext<CR>zz")
vim.keymap.set("n", "<leader>j", "<cmd>lprev<CR>zz")

vim.keymap.set("n", "<leader>s", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]])
vim.keymap.set("n", "<leader>x", "<cmd>!chmod +x %<CR>", { silent = true })

vim.keymap.set("n", "<leader><leader>", function()
    vim.cmd("so")
end)

-- mute highlights
-- vim.keymap.set("n", "C-l", ":noh<CR><c-lvigateUp
-- >")

-- tmux navigator
vim.keymap.set("n", "<A-h>", ":TmuxNavigateLeft<CR>")
vim.keymap.set("n", "<A-j>", ":TmuxNavigateDown<CR>")
vim.keymap.set("n", "<A-k>", ":TmuxNavigateUp<CR>")
vim.keymap.set("n", "<A-l>", ":TmuxNavigateRight<CR>")
--[[
vim.keymap.set("v", "<a-h>", "<c-\><c-n>", "TmuxNavigateLeft<CR>")
vim.keymap.set("v", "<a-j>", "<c-\><c-n>", "TmuxNavigateDown<CR>")
vim.keymap.set("v", "<a-k>", "<c-\><c-n>", "TmuxNavigateUp<CR>")
vim.keymap.set("v", "<a-l>", "<c-\><c-n>", "TmuxNavigateRight<CR>")
vim.keymap.set("i", "<a-h>", "<c-\><c-n>", "TmuxNavigateLeft<CR>")
vim.keymap.set("i", "<a-j>", "<c-\><c-n>", "TmuxNavigateDown<CR>")
vim.keymap.set("i", "<a-k>", "<c-\><c-n>", "TmuxNavigateUp<CR>")
vim.keymap.set("i", "<a-l>", "<c-\><c-n>", "TmuxNavigateRight<CR>")
vim.keymap.set("c", "<a-h>", "<c-\><c-n>", "TmuxNavigateLeft<CR>")
vim.keymap.set("c", "<a-j>", "<c-\><c-n>", "TmuxNavigateDown<CR>")
vim.keymap.set("c", "<a-k>", "<c-\><c-n>", "TmuxNavigateUp<CR>")
vim.keymap.set("c", "<a-l>", "<c-\><c-n>", "TmuxNavigateRight<CR>")
]]--

--[[
if has('nvim')
	vim.keymap.set("t", <a-h> <c-\><c-n>:TmuxNavigateLeft<CR>
	vim.keymap.set("t", <a-j> <c-\><c-n>:TmuxNavigateDown<CR>
	vim.keymap.set("t", <a-k> <c-\><c-n>:TmuxNavigateUp<CR>
	vim.keymap.set("t", <a-l> <c-\><c-n>:TmuxNavigateRight<CR>
	vim.keymap.set("t", <Esc> <c-\><c-n>
endif
]]--
