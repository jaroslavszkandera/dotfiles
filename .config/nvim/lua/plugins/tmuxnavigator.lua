return {
  {
    'christoomey/vim-tmux-navigator',
    config = function()
      -- use custom bindings
      vim.g.tmux_navigator_no_mappings = 1

      -- disable tmux navigator when zomming the Vim pane
      vim.g.tmux_navigator_disable_when_zoomed = 1
    end,
  },
}
