.PHONY: data test help clean

help:
	@echo "Available targets:"
	@echo "  make data - Generate dataset images"
	@echo "  make test - Run tests"
	@echo "  make clean - Remove generated data"
	@echo "  make budget - Show budget calculations"
	@echo "  make metrics - Test metrics module"

data:
	@echo "Generating dataset..."
	python3 make_data.py

test:
	@echo "Running tests..."
	python3 -m pytest tests/ -v

budget:
	python3 budget.py --set data/

metrics:
	python3 metrics.py

clean:
	@echo "Cleaning..."
	rm -rf data/*
	@echo "Done"

data-stats:
	@echo "Data directory contents:"
	ls -lah data/
