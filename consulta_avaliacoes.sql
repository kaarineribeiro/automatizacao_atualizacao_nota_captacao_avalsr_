select tb_avaliacoes.IDColaborador Id
	   , tb_avaliacoes.Colaborador No_Socio
	   , tb_avaliacoes.NivelCaptacaoClientes Nu_NivelCaptacaoSocio

from FactAvaliacaoAnualSRConsultores as tb_avaliacoes

where AnoAvaliacao = 2024