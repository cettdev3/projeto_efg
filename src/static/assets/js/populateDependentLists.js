document.addEventListener('DOMContentLoaded', function () {
    const id_escola = document.getElementById('id_escola');
    populateDependentLists(id_escola);
})

function populateDependentLists(source) {
    const id_escola = $('#id_escola').val();
    const id_tipo_curso = $('#id_tipo_curso').val();
    const id_modalidade = $('#id_modalidade').val();
    const id_eixo = $('#id_eixo').val();
    const id_curso = $('#id_curso').val();

    if (source.id === 'id_escola' || source.id === 'id_tipo_curso' || source.id === 'id_modalidade') {
        popularEixo(id_escola, id_eixo);
        popularCurso(id_escola, id_tipo_curso, id_modalidade, id_eixo, id_curso);
    }

    if (source.id === 'id_eixo') {
        popularCurso(id_escola, id_tipo_curso, id_modalidade, id_eixo, id_curso);
    }

    function popularCurso(id_escola, id_tipo_curso, id_modalidade, id_eixo, id_curso) {
        $.ajax({
            url: '/ajax/get_cursos/',
            type: 'GET',
            data: {
                'id_escola': id_escola,
                'id_tipo_curso': id_tipo_curso,
                'id_modalidade': id_modalidade,
                'id_eixo': id_eixo
            },
            success: function (data) {
                $('#id_curso').empty();
                $('#id_curso').append('<option value="">---------</option>');
                $.each(data, function (key, value) {
                    $('#id_curso').append('<option value="' + value.id + '">' + value.curso + '</option>');
                });
                if (id_curso !== '') {
                    $('#id_curso').val(id_curso);
                }
            }
        });
    };

    function popularEixo(id_escola, id_eixo) {
        $.ajax({
            url: '/ajax/get_eixos/',
            type: 'GET',
            data: {
                'id_escola': id_escola
            },
            success: function (data) {
                $('#id_eixo').empty();
                $('#id_eixo').append('<option value="">---------</option>');
                $.each(data, function (key, value) {
                    $('#id_eixo').append('<option value="' + value.eixo_id + '">' + value.nome + '</option>');
                });
                if (id_eixo !== '') {
                    $('#id_eixo').val(id_eixo);
                }
            }
        });
    };


}