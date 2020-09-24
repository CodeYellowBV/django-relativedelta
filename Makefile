.PHONY: help buil
.DEFAULT_GOAL := help


help:
	@echo "Bumps version"


bump:
	@while :; do \
		read -r -p "bumpversion [major/minor/patch]: " PART; \
		case "$$PART" in \
			major|minor|patch) break ;; \
  		esac \
	done ; \
	bumpversion --no-commit --allow-dirty $$PART
