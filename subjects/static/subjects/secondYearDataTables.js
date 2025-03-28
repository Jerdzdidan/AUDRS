$(document).ready(function() {
    // ==================== secondYear DataTable ====================
    const $secondYearDataTable = $('#secondYearDataTable').DataTable({
        order: [6, 'asc'],
        layout: {
            topStart: null,
            topEnd: null,
            bottomStart: null,
            bottomEnd: null,
            bottom: null,
        },
        language: {
            emptyTable: "No data available in table"
        }
    });

    const $secondYearEntries = $('#secondYearCustomEntries');
    const $secondYearSearch = $('#secondYearSearchBar');
    const $secondYearPagination = $('#secondYearCustomPagination');

    $secondYearEntries.on('change', function() {
        $secondYearDataTable.page.len(parseInt(this.value, 10)).draw();
    });

    $secondYearSearch.on('keyup', function() {
        $secondYearDataTable.search(this.value).draw();
    });

    // Pagination Function
    function updatesecondYearPagination() {
        const info = $secondYearDataTable.page.info();
        let paginationHtml = '<ul class="pagination justify-content-start ms-2">';
        
        // Previous Button
        if (info.page > 0) {
            paginationHtml += `<li class="page-item">
                <a class="page-link text-success" data-page="${info.page-1}" href="#">Prev</a>
            </li>`;
        }

        // Page Numbers
        for (let i = 0; i < info.pages; i++) {
            paginationHtml += `<li class="page-item ${i === info.page ? 'active' : ''}">
                <a class="page-link ${i === info.page ? 'bg-success text-white' : 'text-success'}" 
                   data-page="${i}" href="#">${i+1}</a>
            </li>`;
        }

        // Next Button
        if (info.page < info.pages - 1) {
            paginationHtml += `<li class="page-item">
                <a class="page-link text-success" data-page="${info.page+1}" href="#">Next</a>
            </li>`;
        }
        
        $secondYearPagination.html(paginationHtml + '</ul>');
    }

    // Stock Pagination Events
    $secondYearDataTable.on('draw', updatesecondYearPagination);
    $secondYearPagination.on('click', 'a.page-link', function(e) {
        e.preventDefault();
        $secondYearDataTable.page(parseInt($(this).data('page'), 10)).draw('page');
    });
    updatesecondYearPagination();


});