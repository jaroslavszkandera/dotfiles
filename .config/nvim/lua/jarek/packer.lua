vim.cmd.packadd('packer.nvim')

return require('packer').startup(function(use)
  use 'wbthomason/packer.nvim'

  use {
    'nvim-telescope/telescope.nvim', tag = '0.1.2',
    requires = { { 'nvim-lua/plenary.nvim' } }
  }

  use({
    'cocopon/iceberg.vim',
    as = 'iceberg',
    config = function()
      vim.cmd('colorscheme iceberg')
    end
  })

  -- use ({'catppuccin/nvim',
  --       as = 'catppucin',
  --     config = function()
  --     vim.cmd('colorscheme catppuccin-latte')
  --   end
  -- })

  use{'neoclide/coc.nvim', branch = 'release'}
  use('theprimeagen/harpoon')
  use('mbbill/undotree')
  use('tpope/vim-fugitive')
  use('christoomey/vim-tmux-navigator')
  use('tpope/vim-commentary')
  use {
    'github/copilot.vim',
    config = function()
      vim.g.copilot_enabled = false
    end
  }
end)
