$(document).ready(function() {
    // ==================== minorSubCheckList DataTable ====================
    const $minorSubCheckListDataTable = $('#minorSubCheckListDataTable').DataTable({
        order: [0, 'asc'],
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

    const $minorSubCheckListEntries = $('#minorSubCheckListCustomEntries');
    const $minorSubCheckListSearch = $('#minorSubCheckListSearchBar');
    const $minorSubCheckListPagination = $('#minorSubCheckListCustomPagination');

    $minorSubCheckListEntries.on('change', function() {
        $minorSubCheckListDataTable.page.len(parseInt(this.value, 10)).draw();
    });

    $minorSubCheckListSearch.on('keyup', function() {
        $minorSubCheckListDataTable.search(this.value).draw();
    });

    // Pagination Function
    function updateminorSubCheckListPagination() {
        const info = $minorSubCheckListDataTable.page.info();
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
        
        $minorSubCheckListPagination.html(paginationHtml + '</ul>');
    }

    // Stock Pagination Events
    $minorSubCheckListDataTable.on('draw', updateminorSubCheckListPagination);
    $minorSubCheckListPagination.on('click', 'a.page-link', function(e) {
        e.preventDefault();
        $minorSubCheckListDataTable.page(parseInt($(this).data('page'), 10)).draw('page');
    });
    updateminorSubCheckListPagination();


});