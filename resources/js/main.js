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
        let operationType = $('#operation').value;
        let image = $('#image').value;
        let cutoff = $('#cutoff').value || 0;
        let windowSize = $('#windowSize').value || 0;
        let statisticalFilter = $('#statistical-filter').value || 0;
        let smoothingFilter = $('#smoothing-filter').value || 0;
        let order = $('#order').value || 2;
        this.filterParams = {
            image,
            operationType,
            cutoff,
            windowSize,
            statisticalFilter,
            smoothingFilter,
            order
        };
        $('.source-image').attr('src', '/controllers/assets/images/' + image);
    }

    setEventListeners() {
        this.operationTypeElem.addEventListener('input', event => this.updateOperationType(event));
        this.imageElem.addEventListener('input', event => this.updateImage(event));
        this.cutoffElem.addEventListener('input', event => this.validateCutoff(event));
        this.orderElem.addEventListener('input', event => this.validateOrder(event));
        this.windowSizeElem.addEventListener('input', event => this.validateWindowSize(event));
        this.statisticalFilterElem.addEventListener('input', event => this.validateFilter(event));
        this.smoothingFilterElem.addEventListener('input', event => this.validateFilter(event));
        $('#submit').addEventListener('click', () => this.handleSubmit(event));
    }

    /**
     * Hongwei
     * Operation: Statistical Order Filter
     * Params: {
     *      Filter: [median, mean, adaptive]
     *      Window Size: [3x3, 5x5, and 7x7]
     * }
     */

    /**
     * Tyler Do
     * For my parameters I just the image, window size, and which mean filter (the 1/9 or (1/16 we discussed on the slides)
     * Operation: Smoothing
     * Params: {
     *      Mean Filter: [1/9, 1/16]
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

    static sanitize(input) {
        return input.replace(/\D+/gi, '');
    }

    validateCutoff(event) {
        this.filterParams.cutoff = Form.sanitize(event.target.value);
    }

    validateOrder(event) {
        this.filterParams.order = Form.sanitize(event.target.value);
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
                paths.forEach((path) => {
                    let imageHTML = '';
                    imageHTML += '<div class="column">';
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