// if (!String.prototype.startsWith) {
//   Object.defineProperty(String.prototype, 'startsWith', {
//     value: function(search, pos) {
//       pos = !pos || pos < 0 ? 0 : +pos;
//       return this.substring(pos, pos + search.length) === search;
//     }
//   });
// }

$(document).ready(function(){console.log('FFS')});

$(function() {
    console.log('SOMETHING HAPPENS MAYBE');

  // We store the data-row values as sphinx-data-<data-row value>
  // Add data-row attribute with the extracted value
  $('.sphinx-accordion.title').each(function() {
    const this1 = $(this);
    const prefix = 'sphinx-accordion-title-';
    const classes = this1.attr('class').split(/\s+/);
    $.each(classes, function(idx, clazz) {
      if (clazz.startsWith(prefix)) {
        this1.attr('data-row', clazz.substring(prefix.length));
      }
    });

    const data_row = this1.attr('data-row');

    this1.on('click', function() {
      // Find offset in view
      const offset = (this1.offset().top - $(window).scrollTop());

      // Toggle active class on this subsequent sibling
      if (this1.hasClass('active')) {
        this1.removeClass('active');
        this1.next().removeClass('active');
      } else {
        this1.addClass('active');
        this1.next().addClass('active');
      }

      // Keep tab with the original view offset
      $(window).scrollTop(this1.offset().top - offset);
    });
  });
});