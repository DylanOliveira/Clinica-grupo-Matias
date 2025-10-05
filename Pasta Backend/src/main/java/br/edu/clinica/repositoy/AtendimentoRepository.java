package br.edu.clinica.repository;

import br.edu.clinica.model.Atendimento;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AtendimentoRepository extends JpaRepository<Atendimento, Long> {
    boolean existsByUsuarioId(Long usuarioId);
    boolean existsByProcedimentosContaining(Object procedimento);
}
