// Only load data that's visible
        function lazyLoadCharts() {
            // Only initialize charts when in viewport
            const observers = [];
            document.querySelectorAll('canvas').forEach(canvas => {
                const observer = new IntersectionObserver(entries => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            // Initialize chart when visible
                            initializeChart(canvas.id);
                            observer.disconnect();
                        }
                    });
                });
                observer.observe(canvas);
                observers.push(observer);
            });
        }
        
        document.addEventListener('DOMContentLoaded', lazyLoadCharts);
        