-- select Fk_CaptadorProjetoEspaiderId Num_CaptadorID
-- 	   , No_CaptadorProjeto No_CaptadorProjeto
-- 	   , Nu_AnoReferencia
-- 	   , SUM(Vl_ValorTotalCaptado) Vl_ValorTotalCaptadoAno

-- from View_ClienteProjetoCaptadorValorCaptado

-- where Nu_AnoReferencia = $ano_referencia

-- group by No_CaptadorProjeto, Fk_CaptadorProjetoEspaiderId, Nu_AnoReferencia
-- order by No_CaptadorProjeto, Fk_CaptadorProjetoEspaiderId, Nu_AnoReferencia


with tb_captacoes as 
(
select Fk_CaptadorProjetoEspaiderId Id
	   , No_CaptadorProjeto No_CaptadorProjeto
	   , Nu_AnoReferencia
	   , SUM(Vl_ValorTotalCaptado) Vl_ValorTotalCaptadoAno

from View_ClienteProjetoCaptadorValorCaptado

group by No_CaptadorProjeto, Fk_CaptadorProjetoEspaiderId, Nu_AnoReferencia
--order by No_CaptadorProjeto, Fk_CaptadorProjetoEspaiderId, Nu_AnoReferencia
)

select tb_avaliacoes.IDColaborador Id
	   , tb_avaliacoes.Colaborador No_Socio
	   , IIF(tb_captacoes.Vl_ValorTotalCaptadoAno is null, 0.00, tb_captacoes.Vl_ValorTotalCaptadoAno) Vl_ValorTotalCaptadoAno

from FactAvaliacaoAnualSRConsultores as tb_avaliacoes

left join tb_captacoes
on tb_avaliacoes.IDColaborador = tb_captacoes.Id
   and tb_avaliacoes.AnoAvaliacao = tb_captacoes.Nu_AnoReferencia

where tb_avaliacoes.AnoAvaliacao = $ano_referencia