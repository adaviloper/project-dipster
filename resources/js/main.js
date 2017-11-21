class Form {
    constructor() {
        this.toggleable = ['window-size', 'statistical-filter', 'smoothing-filter', 'k-size', 'cutoff', 'order', 'ssim'];
        this.filterParams = {};
        this.imageElem = document.getElementById('image');
        this.operationTypeElem = document.getElementById('operation');
        this.kSizeElem = document.getElementById('kSize');
        this.cutoffElem = document.getElementById('cutoff');
        this.windowSizeElem = document.getElementById('windowSize');
        this.statisticalFilterElem = document.getElementById('statistical-filter');
        this.smoothingFilterElem = document.getElementById('smoothing-filter');
        this.orderElem = document.getElementById('order');
        this.setDefaultValues();
        this.toggleOptions();
        this.setEventListeners();
    }

    setDefaultValues() {
        let operationType = document.getElementById('operation').value;
        let image = document.getElementById('image').value;
        let kSize = document.getElementById('kSize').value;
        let cutoff = document.getElementById('cutoff').value || 0;
        let windowSize = document.getElementById('windowSize').value;
        let statisticalFilter = document.getElementById('statistical-filter').value;
        let smoothingFilter = document.getElementById('smoothing-filter').value;
        let order = document.getElementById('order').value || 2;
        this.filterParams = {
            image,
            operationType,
            kSize,
            cutoff,
            windowSize,
            statisticalFilter,
            smoothingFilter,
            order
        };
        $('.source-image').attr('src', '/controllers/assets/images/' + image);
    }

    setEventListeners() {
        document.getElementById('operation').addEventListener('input', event => this.updateOperationType(event));
        document.getElementById('image').addEventListener('input', event => this.updateImage(event));
        document.getElementById('kSize').addEventListener('input', event => this.validateKSize(event));
        document.getElementById('cutoff').addEventListener('input', event => this.validateCutoff(event));
        document.getElementById('order').addEventListener('input', event => this.validateOrder(event));
        document.getElementById('windowSize').addEventListener('input', event => this.validateWindowSize(event));
        document.getElementById('statistical-filter').addEventListener('input', event => this.validateStatisticalFilter(event));
        document.getElementById('smoothing-filter').addEventListener('input', event => this.validateSmoothingFilter(event));
        // document.getElementById('ssim').addEventListener('input', event => this.validateSSIM(event));
        // $('#ssim').keypress((event) => {
        //   if ((event.which !== 46 || $('#ssim').val().indexOf('.') !== -1) && (event.which < 48 || event.which > 57)) {
        //     event.preventDefault();
        //   }
        //   this.filterParams.ssim = $('#ssim').val();
        // });
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
        this.toggleable.forEach((name) => {
            this.toggleDisplay(name, 'none');
        });
        if(this.filterParams.operationType === 'smoothing') {
            this.toggleDisplay('smoothing-filter', 'block');
            this.toggleDisplay('window-size', 'block');
        } else if(this.filterParams.operationType === 'statistical-order-filtering') {
            this.toggleDisplay('statistical-filter', 'block');
            this.toggleDisplay('window-size', 'block');
        } else if(this.filterParams.operationType === 'laplacian') {
        } else if(this.filterParams.operationType === 'unsharp') {
            this.toggleDisplay('window-size', 'block');
        } else if(this.filterParams.operationType === 'first-order-derivatives') {
            this.toggleDisplay('window-size', 'block');
            this.toggleDisplay('k-size', 'block');
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

    validateKSize(event) {
        this.filterParams.kSize = event.target.value;
        this.kSizeElem.value = this.filterParams.kSize;
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

    validateStatisticalFilter(event) {
        this.filterParams.statisticalFilter = event.target.value;
    }

    validateSmoothingFilter(event) {
        this.filterParams.smoothingFilter = event.target.value;
    }

    updateParams() {
        this.filterParams.cutoff = this.cutoffElem.value;
        this.filterParams.order = this.orderElem.value;
    }

    handleSubmit() {
        this.updateParams();
        $('.result-image').remove();
        $('.results-wrapper').append('<div class="column result-image"><img src="/controllers/assets/images/loading-spinner.gif" /></div>');
        $.ajax({
            url: `http://localhost:8080/${this.filterParams.operationType}`,
            data: this.filterParams,
            success: function(data) {
                console.log(data)
                $('.result-image').remove();
                let paths = data.slice(1).slice(0, -1).replace("\r\n\r\n", "\n\n").split("\n\n");
                paths.forEach((path) => {
                    let params = path.split('?')[1];
                    if(params) {
                        path=path.split('?')[0];
                        console.log(path)
                        params = JSON.parse('{"' + decodeURI(params).replace(/"/g, '\\'").replace(/&/g, '","').replace(/=/g,'":"') + '"}');

                    }
                    let imageHTML = '';
                    imageHTML += '<div class="column result-image">';
                    imageHTML += '<img src="' + path + '" alt="" class="image image-out">';
                    for(let key in params) {
                        imageHTML += "<strong>" + key + "</strong>: " + params[key] + "<br/>";
                    }
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