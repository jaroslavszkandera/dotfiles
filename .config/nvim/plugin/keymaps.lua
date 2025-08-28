-- while in normal mode, press "<leader>pv" it will execute this command
vim.keymap.set("n", "<leader>pv", vim.cmd.Ex)

-- move things in visual mode
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

-- movement settings
vim.keymap.set("n", "J", "mzJ`z")
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")
vim.keymap.set("n", "n", "nzzzv")
vim.keymap.set("n", "N", "Nzzzv")

-- replace with paste or delete without losing the register
vim.keymap.set("x", "<leader>p", [["_dP]])
vim.keymap.set({ "n", "v" }, "<leader>d", [["_d]])

-- format the code
vim.keymap.set("n", "<leader>f", vim.lsp.buf.format)

-- TODO
-- navigate quickfix or location list
-- vim.keymap.set("n", "<C-k>", "<cmd>lnext<CR>zz")
-- vim.keymap.set("n", "<C-j>", "<cmd>lprev<CR>zz")
vim.keymap.set("n", "<leader>j", "<cmd>cnext<CR>zz")
vim.keymap.set("n", "<leader>k", "<cmd>cprev<CR>zz")

vim.keymap.set("n", "<leader>s", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]])
vim.keymap.set("n", "<leader>x", "<cmd>!chmod +x %<CR>", { silent = true })

vim.keymap.set("n", "<leader><leader>", function()
  vim.cmd("so") -- source the file
end)

-- mute highlights
vim.keymap.set("n", "<leader>l", ":noh<CR><c-lvigateUp")
-- vim.keymap.set("n", "<C-l>", ":noh<CR><c-lvigateUp") -- does not function

-- tmux navigator
vim.keymap.set("n", "<A-h>", ":TmuxNavigateLeft<CR>")
vim.keymap.set("n", "<A-j>", ":TmuxNavigateDown<CR>")
vim.keymap.set("n", "<A-k>", ":TmuxNavigateUp<CR>")
vim.keymap.set("n", "<A-l>", ":TmuxNavigateRight<CR>")

vim.keymap.set("v", "<A-h>", "<C-\\><C-n>:TmuxNavigateLeft<CR>")
vim.keymap.set("v", "<A-j>", "<C-\\><C-n>:TmuxNavigateDown<CR>")
vim.keymap.set("v", "<A-k>", "<C-\\><C-n>:TmuxNavigateUp<CR>")
vim.keymap.set("v", "<A-l>", "<C-\\><C-n>:TmuxNavigateRight<CR>")
vim.keymap.set("i", "<A-h>", "<C-\\><C-n>:TmuxNavigateLeft<CR>")
vim.keymap.set("i", "<A-j>", "<C-\\><C-n>:TmuxNavigateDown<CR>")
vim.keymap.set("i", "<A-k>", "<C-\\><C-n>:TmuxNavigateUp<CR>")
vim.keymap.set("i", "<A-l>", "<C-\\><C-n>:TmuxNavigateRight<CR>")
vim.keymap.set("c", "<A-h>", "<C-\\><C-n>:TmuxNavigateLeft<CR>")
vim.keymap.set("c", "<A-j>", "<C-\\><C-n>:TmuxNavigateDown<CR>")
vim.keymap.set("c", "<A-k>", "<C-\\><C-n>:TmuxNavigateUp<CR>")
vim.keymap.set("c", "<A-l>", "<C-\\><C-n>:TmuxNavigateRight<CR>")

if vim.fn.has('nvim') then
  vim.keymap.set("t", "<A-h>", "<C-\\><C-n>:TmuxNavigateLeft<CR>")
  vim.keymap.set("t", "<A-j>", "<C-\\><C-n>:TmuxNavigateDown<CR>")
  vim.keymap.set("t", "<A-k>", "<C-\\><C-n>:TmuxNavigateUp<CR>")
  vim.keymap.set("t", "<A-l>", "<C-\\><C-n>:TmuxNavigateRight<CR>")
  vim.keymap.set("t", "<Esc>", "<C-\\><C-n>")
end
