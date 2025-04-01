$(document).ready(function() {
    // ==================== firstYearCheckList DataTable ====================
    const $firstYearCheckListDataTable = $('#firstYearCheckListDataTable').DataTable({
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

    const $firstYearCheckListEntries = $('#firstYearCheckListCustomEntries');
    const $firstYearCheckListSearch = $('#firstYearCheckListSearchBar');
    const $firstYearCheckListPagination = $('#firstYearCheckListCustomPagination');

    $firstYearCheckListEntries.on('change', function() {
        $firstYearCheckListDataTable.page.len(parseInt(this.value, 10)).draw();
    });

    $firstYearCheckListSearch.on('keyup', function() {
        $firstYearCheckListDataTable.search(this.value).draw();
    });

    // Pagination Function
    function updatefirstYearCheckListPagination() {
        const info = $firstYearCheckListDataTable.page.info();
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
        
        $firstYearCheckListPagination.html(paginationHtml + '</ul>');
    }

    // Stock Pagination Events
    $firstYearCheckListDataTable.on('draw', updatefirstYearCheckListPagination);
    $firstYearCheckListPagination.on('click', 'a.page-link', function(e) {
        e.preventDefault();
        $firstYearCheckListDataTable.page(parseInt($(this).data('page'), 10)).draw('page');
    });
    updatefirstYearCheckListPagination();


});