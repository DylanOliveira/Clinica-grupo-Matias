package br.edu.clinica.service;

import br.edu.clinica.model.Atendimento;
import br.edu.clinica.model.Procedimento;
import br.edu.clinica.repository.AtendimentoRepository;
import br.edu.clinica.repository.ProcedimentoRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.Set;

@Service
public class AtendimentoService {

    private final AtendimentoRepository repo;
    private final ProcedimentoRepository procedimentoRepo;

    public AtendimentoService(AtendimentoRepository repo, ProcedimentoRepository procedimentoRepo) {
        this.repo = repo;
        this.procedimentoRepo = procedimentoRepo;
    }

    public Atendimento salvar(Atendimento a) {
        
        if (a.getProcedimentos() == null || a.getProcedimentos().isEmpty()) {
            throw new IllegalArgumentException("Atendimento deve ter ao menos um procedimento");
        }

        
        if ("plano".equals(a.getTipo()) && (a.getNumeroCarteira() == null || a.getNumeroCarteira().isBlank())) {
            throw new IllegalArgumentException("Número da carteira é obrigatório para atendimento por plano");
        }

        
        BigDecimal total = BigDecimal.ZERO;
        for (Procedimento p : a.getProcedimentos()) {
            Procedimento proc = procedimentoRepo.findById(p.getId()).orElseThrow();
            if ("plano".equals(a.getTipo())) {
                total = total.add(proc.getValorPlano());
            } else {
                total = total.add(proc.getValorParticular());
            }
        }
        a.setValorTotal(total);

        return repo.save(a);
    }

    public List<Atendimento> listar() {
        return repo.findAll();
    }
}
