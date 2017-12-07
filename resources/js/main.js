class Form {
    constructor() {
        this.toggleable = ['window-size', 'unsharp-filter-type', 'statistical-filter', 'smoothing-filter', 'cutoff', 'order', 'ssim', 'high-boost-filter-type', 'first-order-filter-type'];
        this.filterParams = {};
        this.imageElem = document.getElementById('image');
        this.operationTypeElem = document.getElementById('operation');
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
        let cutoff = document.getElementById('cutoff').value || 0;
        let windowSize = document.getElementById('windowSize').value;
        let unsharpFilterType = document.getElementById('unsharpFilterType').value;
        let statisticalFilter = document.getElementById('statistical-filter').value;
        let smoothingFilter = document.getElementById('smoothing-filter').value;
        let filterOperator = document.getElementById('first-order-filter-type').value;
        let highBoostFilterType = document.getElementById('high-boost-filter-type').value;
        let order = document.getElementById('order').value || 2;
        this.filterParams = {
            image,
            operationType,
            cutoff,
            windowSize,
            unsharpFilterType,
            statisticalFilter,
            smoothingFilter,
            order,
            filterOperator,
            highBoostFilterType
        };
        $('.source-image').attr('src', '/controllers/assets/images/' + image);
    }

    setEventListeners() {
        document.getElementById('operation').addEventListener('input', event => this.updateOperationType(event));
        document.getElementById('image').addEventListener('input', event => this.updateImage(event));
        document.getElementById('cutoff').addEventListener('input', event => this.validateCutoff(event));
        document.getElementById('order').addEventListener('input', event => this.validateOrder(event));
        document.getElementById('windowSize').addEventListener('input', event => this.validateWindowSize(event));
        document.getElementById('unsharpFilterType').addEventListener('input', event => this.validateUnsharpFilterType(event));
        document.getElementById('statistical-filter').addEventListener('input', event => this.validateStatisticalFilter(event));
        document.getElementById('smoothing-filter').addEventListener('input', event => this.validateSmoothingFilter(event));
        document.getElementById('first-order-filter-type').addEventListener('input', event => this.validateFirstOrderFilterOperator(event));
        document.getElementById('high-boost-filter-type').addEventListener('input', event => this.validateHighBoostFilterType(event));
        // document.getElementById('ssim').addEventListener('input', event => this.validateSSIM(event));
        // $('#ssim').keypress((event) => {
        //   if ((event.which !== 46 || $('#ssim').val().indexOf('.') !== -1) && (event.which < 48 || event.which > 57)) {
        //     event.preventDefault();
        //   }
        //   this.filterParams.ssim = $('#ssim').val();
        // });
        document.getElementById('submit').addEventListener('click', () => this.handleSubmit(event));
    }

    updateOperationType(event) {
        this.filterParams.operationType = event.target.value;
        this.toggleOptions();
    }

    toggleOptions() {
        this.toggleable.forEach((name) => {
            this.toggleDisplay(name, 'none');
        });
        if (this.filterParams.operationType === 'smoothing') {
            // this.toggleDisplay('smoothing-filter', 'block');
            this.toggleDisplay('window-size', 'block');
        } else if (this.filterParams.operationType === 'statistical-order-filtering') {
            this.toggleDisplay('statistical-filter', 'block');
            this.toggleDisplay('window-size', 'block');
        } else if (this.filterParams.operationType === 'laplacian') {
        } else if (this.filterParams.operationType === 'unsharp') {
            this.toggleDisplay('window-size', 'block');
            this.toggleDisplay('unsharp-filter-type', 'block');
            this.toggleDisplay('high-boost-filter-type', 'block');
        } else if (this.filterParams.operationType === 'first-order-derivatives') {
            this.toggleDisplay('first-order-filter-type', 'block');
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

    validateUnsharpFilterType(event) {
        this.filterParams.unsharpFilterType = event.target.value;
        if(this.filterParams.unsharpFilterType === 'gaussian') {
            this.toggleDisplay('gaussian-sub', 'none');
        } else {
            this.toggleDisplay('gaussian-sub', 'block');
        }
    }

    validateStatisticalFilter(event) {
        this.filterParams.statisticalFilter = event.target.value;
    }

    validateSmoothingFilter(event) {
        this.filterParams.smoothingFilter = event.target.value;
    }

    validateFirstOrderFilterOperator(event) {
        this.filterParams.firstOrderFilterOperator = event.target.value;
    }

    validateHighBoostFilterType(event) {
        this.filterParams.highBoostFilterType = event.target.value;
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
            success: function (data) {
                console.log(data)
                $('.result-image').remove();
                let paths = data.slice(1).slice(0, -1).replace("\r\n\r\n", "\n\n").split("\n\n");
                paths.forEach((path) => {
                    let params = path.split('?')[1];
                    if (params) {
                        params = JSON.parse('{"' + decodeURI(params).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g, '":"') + '"}');


                    }
                    let imageHTML = '';
                    imageHTML += '<div class="column result-image">';
                    imageHTML += '<img src="' + path + '" alt="" class="image image-out">';
                    for (let key in params) {
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