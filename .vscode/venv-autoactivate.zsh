# Auto-activate project virtualenv when entering this workspace.
# Safe to source multiple times.

if [[ -n "${_DISTRIBUTIONGROUP_VENV_HOOK_LOADED:-}" ]]; then
  return
fi
_DISTRIBUTIONGROUP_VENV_HOOK_LOADED=1

_distributiongroup_workspace="/Users/bobwillmot/src/distributiongroup"
_distributiongroup_activate_venv() {
  if [[ "$PWD" == "${_distributiongroup_workspace}"(|/*) ]]; then
    if [[ -f "${_distributiongroup_workspace}/.venv/bin/activate" ]]; then
      if [[ "${VIRTUAL_ENV:-}" != "${_distributiongroup_workspace}/.venv" ]]; then
        source "${_distributiongroup_workspace}/.venv/bin/activate"
      fi
    fi
  fi
}

autoload -Uz add-zsh-hook
add-zsh-hook chpwd _distributiongroup_activate_venv
_distributiongroup_activate_venv
