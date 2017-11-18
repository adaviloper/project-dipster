class Form {
    constructor() {
        this.toggleable = ['windowSize', 'statistical-filter', 'smoothing-filter', 'cutoff', 'order'];
        this.filterParams = {};
        this.imageElem = $('#image');
        this.operationTypeElem = $('#operation');
        this.cutoffElem = $('#cutoff');
        this.windowSizeElem = $('#windowSize');
        this.statisticalFilterElem = $('#statistical-filter');
        this.smoothingFilterElem = $('#smoothing-filter');
        this.orderElem = $('#order');
        this.setDefaultValues();
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
        $('#ssim').keypress(function(event) {
          if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
            event.preventDefault();
          }
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
        }
    }

    updateImage(event) {
        this.filterParams.image = event.target.value;
        $('.source-image').attr('src', '/controllers/assets/images/' + this.filterParams.image);
    }

    toggleDisplay(name, state) {
        $('.' + name + '-wrapper').css('display', state);
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
    }

    validateWindowSize(event) {
        this.filterParams.windowSize = event.target.value;
    }

    validateFilter(event) {
        this.filterParams.filter = event.target.value;
    }

    handleSubmit() {
        $.ajax({
            url: `http://localhost:8080/${this.filterParams.operationType}`,
            data: this.filterParams,
            success: function(data) {
                let paths = data.slice(1).slice(0, -1).split("\n\n");
                console.log(paths);
                $('.result-image').remove();
                paths.forEach((path) => {
//                console.log(path);
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