// $(document).ready(function () {
//     console.log("inside grid")
//     $('#pinBoot').pinterest_grid({
//         no_columns: 3,
//         padding_x: 10,
//         padding_y: 10,
//         margin_bottom: 50,
//         single_column_breakpoint: 700
//     });
// });

/*
Ref:
Thanks to:
http://www.jqueryscript.net/layout/Simple-jQuery-Plugin-To-Create-Pinterest-Style-Grid-Layout-Pinterest-Grid.html
*/
(function ($, window, document, undefined) {
    var pluginName = 'pinterest_grid',
        pluginName1 = 'pinterest_grid1',
        defaults = {
            padding_x: 10,
            padding_y: 10,
            no_columns: 3,
            margin_bottom: 50,
            single_column_breakpoint: 700
        },

        columns,
        $article,
        article_width;

    // var pluginName = 'pinterest_grid',
    // defaults = {
    //       padding_x: 10,
    //       padding_y: 10,
    //       no_columns: 1,
    //       margin_bottom: 50,
    //       single_column_breakpoint: 700
    //   }, 

    //   columns,
    //   $article,
    //   article_width;


    function Plugin(element, options) {
        this.element = element;
        this.options = $.extend({}, defaults, options);
        this._defaults = defaults;
        this._name = pluginName;
        this._name1 = pluginName1;
        this.init();
    }

    Plugin.prototype.init = function () {
        var self = this,
            resize_finish;
        var c = 0;
        for (var i in self.element) {
            // $(window).resize(function () {
            clearTimeout(resize_finish);
            resize_finish = setTimeout(function () {
                self.make_layout_change(self);
            }, 15);
            c++
            if(c == 10) break;
            // clearTimeout(resize_finish);
            // });
        }
        self.make_layout_change(self);
        $(window).resize();
        // setTimeout(function () {
        //     $(window).resize();
        // }, 500);
    };

    Plugin.prototype.calculate = function (single_column_mode) {
        var self = this,
            tallest = 0,
            row = 0,
            $container = $(this.element),
            container_width = $container.width();
        $article = $(this.element).children();

        console.log("inside", self.options.no_columns)
        if (single_column_mode === true) {
            article_width = $container.width() - self.options.padding_x;
        } else {
            article_width = ($container.width() - self.options.padding_x * self.options.no_columns) / self.options.no_columns;
        }

        $article.each(function () {
            $(this).css('width', article_width);
        });

        columns = self.options.no_columns;

        $article.each(function (index) {
            var current_column,
                left_out = 0,
                top = 0,
                $this = $(this),
                prevAll = $this.prevAll(),
                tallest = 0;

            if (single_column_mode === false) {
                current_column = (index % columns);
            } else {
                current_column = 0;
            }

            for (var t = 0; t < columns; t++) {
                $this.removeClass('c' + t);
            }

            if (index % columns === 0) {
                row++;
            }

            $this.addClass('c' + current_column);
            $this.addClass('r' + row);

            prevAll.each(function (index) {
                if ($(this).hasClass('c' + current_column)) {
                    top += $(this).outerHeight() + self.options.padding_y;
                }
            });

            if (single_column_mode === true) {
                console.log("inside");
                left_out = 0;
            } else {
                left_out = (index % columns) * (article_width + self.options.padding_x);
            }

            $this.css({
                'left': left_out,
                'top': top
            });
        });

        this.tallest($container);
        $(window).resize();
    };

    Plugin.prototype.tallest = function (_container) {
        var column_heights = [],
            largest = 0;

        for (var z = 0; z < columns; z++) {
            var temp_height = 0;
            _container.find('.c' + z).each(function () {
                temp_height += $(this).outerHeight();
            });
            column_heights[z] = temp_height;
        }

        largest = Math.max.apply(Math, column_heights);
        _container.css('height', largest + (this.options.padding_y + this.options.margin_bottom));
    };

    Plugin.prototype.make_layout_change = function (_self) {
        if ($(window).width() < _self.options.single_column_breakpoint) {
            _self.calculate(true);
        } else {
            _self.calculate(false);
        }
    };

    $.fn[pluginName] = function (options) {
        console.log("this",options)
        return this.each(function () {
            if (!$.data(this, 'plugin_' + pluginName)) {
                $.data(this, 'plugin_' + pluginName,
                    new Plugin(this, options));
            }
        });
    }

    $.fn[pluginName1] = function (options) {
        console.log("this",options)
        return this.each(function () {
            if (!$.data(this, 'plugin_' + pluginName1)) {
                $.data(this, 'plugin_' + pluginName1,
                    new Plugin(this, options));
            }
        });
    }
})(jQuery, window, document);