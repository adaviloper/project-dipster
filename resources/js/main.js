class Form {
    constructor() {
        this.toggleable = ['window-size', 'statistical-filter', 'smoothing-filter', 'cutoff', 'order', 'ssim'];
        this.filterParams = {};
        this.imageElem = document.getElementById('image');
        this.operationTypeElem = document.getElementById('operation');
        this.cutoffElem = document.getElementById('cutoff');
        this.windowSizeElem = document.getElementById('windowSize');
        this.statisticalFilterElem = document.getElementById('statistical-filter');
        this.smoothingFilterElem = document.getElementById('smoothing-filter');
        this.orderElem = document.getElementById('order');
        this.ssimElem = document.getElementById('ssim');
        this.setDefaultValues();
        this.toggleOptions();
        this.setEventListeners();
    }

    setDefaultValues() {
        let operationType = document.getElementById('operation').value;
        let image = document.getElementById('image').value;
        let cutoff = document.getElementById('cutoff').value || 0;
        let windowSize = document.getElementById('windowSize').value || 0;
        let statisticalFilter = document.getElementById('statistical-filter').value || 0;
        let smoothingFilter = document.getElementById('smoothing-filter').value || 0;
        let order = document.getElementById('order').value || 2;
        let ssim = document.getElementById('ssim').value || 0;
        this.filterParams = {
            image,
            operationType,
            cutoff,
            windowSize,
            statisticalFilter,
            smoothingFilter,
            order,
            ssim
        };
        $('.source-image').attr('src', '/controllers/assets/images/' + image);
    }

    setEventListeners() {
        document.getElementById('operation').addEventListener('input', event => this.updateOperationType(event));
        document.getElementById('image').addEventListener('input', event => this.updateImage(event));
        document.getElementById('cutoff').addEventListener('input', event => this.validateCutoff(event));
        document.getElementById('order').addEventListener('input', event => this.validateOrder(event));
        document.getElementById('windowSize').addEventListener('input', event => this.validateWindowSize(event));
        document.getElementById('statistical-filter').addEventListener('input', event => this.validateFilter(event));
        document.getElementById('smoothing-filter').addEventListener('input', event => this.validateFilter(event));
        // document.getElementById('ssim').addEventListener('input', event => this.validateSSIM(event));
        $('#ssim').keypress((event) => {
          if ((event.which !== 46 || $('#ssim').val().indexOf('.') !== -1) && (event.which < 48 || event.which > 57)) {
            event.preventDefault();
          }
          this.filterParams.ssim = $('#ssim').val();
        });
        document.getElementById('submit').addEventListener('click', () => this.handleSubmit(event));
    }

    /**
     * Hongwei
     * Operation: Statistical Order Filter
     * Params: {
     *      Filter: [median, mean, adaptive]
     *      Window Size: [3x3, 5x5, and 7x7]
     *      SSIM: Integer
     *
     * }
     */

    /**
     * Tyler Do
     * For my parameters I just the image, window size, and which mean filter (the 1/9 or (1/16 we discussed on the slides)
     * Operation: Smoothing
     * Params: {
     *      X - Mean Filter: [1/9, 1/16]
     *      Window Size: [3x3, 5x5, and 7x7]
     * }
     */
    updateOperationType(event) {
        this.filterParams.operationType = event.target.value;
        this.toggleOptions();
    }

    toggleOptions() {
        if(this.filterParams.operationType === 'smoothing') {
            this.toggleable.forEach((name) => {
                this.toggleDisplay(name, 'none');
            });
            this.toggleDisplay('smoothing-filter', 'block');
            this.toggleDisplay('window-size', 'block');
        } else if(this.filterParams.operationType === 'statistical-order-filtering') {
            this.toggleable.forEach((name) => {
                this.toggleDisplay(name, 'none');
            });
            this.toggleDisplay('statistical-filter', 'block');
            this.toggleDisplay('window-size', 'block');
        } else if(this.filterParams.operationType === 'laplacian') {
            this.toggleable.forEach((name) => {
                this.toggleDisplay(name, 'none');
            });
            this.toggleDisplay('statistical-filter', 'block');
            this.toggleDisplay('window-size', 'block');
        } else if(this.filterParams.operationType === 'unsharp') {
            this.toggleable.forEach((name) => {
                this.toggleDisplay(name, 'none');
            });
            this.toggleDisplay('window-size', 'block');
        }
    }

    toggleDisplay(name, state) {
        $('.' + name + '-wrapper').css('display', state);
    }

    updateImage(event) {
        this.filterParams.image = event.target.value;
        $('.source-image').attr('src', '/controllers/assets/images/' + this.filterParams.image);
    }

    static sanitizeInt(input) {
        return input.replace(/\D+/gi, '');
    }

    validateCutoff(event) {
        this.filterParams.cutoff = Form.sanitizeInt(event.target.value);
        this.cutoffElem.value = this.filterParams.cutoff;
    }

    validateOrder(event) {
        this.filterParams.order = Form.sanitizeInt(event.target.value);
        this.orderElem.value = this.filterParams.order;
    }

    validateWindowSize(event) {
        this.filterParams.windowSize = event.target.value;
    }

    validateFilter(event) {
        this.filterParams.filter = event.target.value;
    }

    updateParams() {
        this.filterParams.ssim = this.ssimElem.value;
        this.filterParams.cutoff = this.cutoffElem.value;
        this.filterParams.order = this.orderElem.value;
    }

    handleSubmit() {
        this.updateParams();
        $.ajax({
            url: `http://localhost:8080/${this.filterParams.operationType}`,
            data: this.filterParams,
            success: function(data) {
                let paths = data.slice(1).slice(0, -1).split("\n\n");
                $('.result-image').remove();
                paths.forEach((path) => {
                    let imageHTML = '';
                    imageHTML += '<div class="column result-image">';
                    imageHTML += '<img src="' + path + '" alt="" class="image image-out">';
                    imageHTML += '</div>';
                    $('.results-wrapper').append(imageHTML);
                });
            },
            error: function (jqXHR, exception) {
                let msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status === 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status === 500) {
                    msg = 'Internal Server Error [500].';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }
                console.error(msg);
            }
        });
    }
}

new Form();