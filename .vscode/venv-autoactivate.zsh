# Auto-activate project virtualenv when entering this workspace.
# Safe to source multiple times.

if [[ -n "${_POSTGRESQL_VENV_HOOK_LOADED:-}" ]]; then
  return
fi
_POSTGRESQL_VENV_HOOK_LOADED=1

_postgresql_workspace="/Users/bobwillmot/src/postgresql"
_postgresql_activate_venv() {
  if [[ "$PWD" == "${_postgresql_workspace}"(|/*) ]]; then
    if [[ -f "${_postgresql_workspace}/.venv/bin/activate" ]]; then
      if [[ "${VIRTUAL_ENV:-}" != "${_postgresql_workspace}/.venv" ]]; then
        source "${_postgresql_workspace}/.venv/bin/activate"
      fi
    fi
  fi
}

autoload -Uz add-zsh-hook
add-zsh-hook chpwd _postgresql_activate_venv
_postgresql_activate_venv
