$(document).ready(function() {
    // ==================== pending DataTable ====================
    const $pendingDataTable = $('#pendingDataTable').DataTable({
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

    const $pendingEntries = $('#pendingCustomEntries');
    const $pendingSearch = $('#pendingSearchBar');
    const $pendingPagination = $('#pendingCustomPagination');

    $pendingEntries.on('change', function() {
        $pendingDataTable.page.len(parseInt(this.value, 10)).draw();
    });

    $pendingSearch.on('keyup', function() {
        $pendingDataTable.search(this.value).draw();
    });

    // Pagination Function
    function updatependingPagination() {
        const info = $pendingDataTable.page.info();
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
        
        $pendingPagination.html(paginationHtml + '</ul>');
    }

    // Stock Pagination Events
    $pendingDataTable.on('draw', updatependingPagination);
    $pendingPagination.on('click', 'a.page-link', function(e) {
        e.preventDefault();
        $pendingDataTable.page(parseInt($(this).data('page'), 10)).draw('page');
    });
    updatependingPagination();


});